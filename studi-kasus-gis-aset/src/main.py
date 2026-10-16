
from __future__ import annotations

from html import escape
from importlib import import_module
from pathlib import Path
import sys
from typing import Any

DataFrame = Any
folium: Any = None
pd: Any = None

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "aset_fasilitas.csv"
OUTPUT_DIR = ROOT / "output"

REQUIRED_COLUMNS = {
    "id_aset", "nama_aset", "kategori",
    "kondisi", "latitude", "longitude",
}

CONDITION_COLORS = {
    "Baik": "#16a34a",
    "Perlu Perawatan": "#f59e0b",
    "Rusak": "#dc2626",
}
DEFAULT_COLOR = "#64748b"


def load_and_validate_data(file_path: Path) -> Any:
    """Membaca dan memvalidasi data fasilitas publik."""
    if not file_path.exists():
        raise FileNotFoundError(f"Data tidak ditemukan: {file_path}")

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError("CSV tidak berisi data aset.")

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            "Kolom wajib tidak ditemukan: "
            + ", ".join(sorted(missing))
        )

    df = df.copy()
    text_columns = ["id_aset", "nama_aset", "kategori", "kondisi"]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    if (
        df[text_columns].isna().any().any()
        or (df[text_columns] == "").any().any()
    ):
        raise ValueError("Ada nilai kosong pada kolom teks wajib.")

    if df["id_aset"].duplicated().any():
        duplicates = df.loc[
            df["id_aset"].duplicated(keep=False), "id_aset"
        ].tolist()
        raise ValueError(f"ID aset duplikat: {duplicates}")

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    if df[["latitude", "longitude"]].isna().any().any():
        raise ValueError("Koordinat harus berupa angka yang valid.")

    valid = (
        df["latitude"].between(-90, 90)
        & df["longitude"].between(-180, 180)
    )
    if not valid.all():
        raise ValueError("Ada koordinat di luar rentang geografis.")

    for column in ["kategori", "kondisi"]:
        df[column] = (
            df[column]
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
            .str.title()
        )

    return df


def add_dashboard_panel(asset_map: Any, df: DataFrame) -> None:
    """Menambahkan statistik dan grafik kategori pada peta."""
    total = len(df)
    good = int((df["kondisi"] == "Baik").sum())
    maintenance = int((df["kondisi"] == "Perlu Perawatan").sum())
    damaged = int((df["kondisi"] == "Rusak").sum())

    category_counts = df["kategori"].value_counts().to_dict()
    max_count = max(category_counts.values()) if category_counts else 1

    bars = ""
    for category, count in sorted(category_counts.items()):
        width = count / max_count * 100
        bars += f"""
        <div class="category-row">
          <div class="category-label">
            <span>{escape(str(category))}</span>
            <b>{count}</b>
          </div>
          <div class="bar-track">
            <div class="bar-fill" style="width:{width:.1f}%"></div>
          </div>
        </div>
        """

    dashboard_html = f"""
    <style>
      .dashboard-panel {{
        position:fixed; top:16px; left:62px; z-index:9999;
        width:300px; max-height:calc(100vh - 32px);
        overflow-y:auto; box-sizing:border-box;
        padding:18px; background:#fff;
        border:1px solid #e2e8f0; border-radius:14px;
        box-shadow:0 6px 24px rgba(15,23,42,.16);
        color:#1e293b; font-family:Arial,sans-serif;
      }}
      .dashboard-panel * {{ box-sizing:border-box; }}
      .dashboard-title {{ font-size:20px; font-weight:700; }}
      .dashboard-subtitle {{
        margin-top:5px; font-size:12px; color:#64748b;
        line-height:1.5;
      }}
      .stat-grid {{
        display:grid; grid-template-columns:1fr 1fr;
        gap:9px; margin-top:16px;
      }}
      .stat-card {{
        border:1px solid #e2e8f0; border-radius:10px;
        padding:11px; background:#f8fafc;
      }}
      .stat-number {{ font-size:25px; font-weight:700; }}
      .stat-label {{ font-size:11px; color:#64748b; margin-top:4px; }}
      .section-title {{
        font-size:13px; font-weight:700; margin:20px 0 12px;
      }}
      .condition-row {{
        display:flex; align-items:center; gap:8px;
        margin:10px 0; font-size:12px;
      }}
      .dot {{
        width:10px; height:10px; border-radius:50%;
        display:inline-block; flex-shrink:0;
      }}
      .category-row {{ margin:12px 0; font-size:12px; }}
      .category-label {{
        display:flex; justify-content:space-between; gap:8px;
        margin-bottom:6px;
      }}
      .bar-track {{
        height:7px; background:#e2e8f0;
        border-radius:10px; overflow:hidden;
      }}
      .bar-fill {{ height:100%; background:#2563eb; border-radius:10px; }}
      .dashboard-note {{
        border-top:1px solid #e2e8f0; margin-top:16px;
        padding-top:12px; color:#64748b;
        font-size:10px; line-height:1.5;
      }}
      @media(max-width:600px) {{
        .dashboard-panel {{
          top:10px; left:54px; width:235px;
          max-height:65vh; padding:12px;
        }}
        .dashboard-title {{ font-size:17px; }}
        .stat-number {{ font-size:21px; }}
      }}
    </style>

    <div class="dashboard-panel">
      <div class="dashboard-title">Peta Fasilitas Publik</div>
      <div class="dashboard-subtitle">
        Dashboard inventaris dan kondisi aset
      </div>

      <div class="stat-grid">
        <div class="stat-card">
          <div class="stat-number">{total}</div>
          <div class="stat-label">Total aset</div>
        </div>
        <div class="stat-card">
          <div class="stat-number" style="color:#16a34a">{good}</div>
          <div class="stat-label">Kondisi baik</div>
        </div>
        <div class="stat-card">
          <div class="stat-number" style="color:#d97706">{maintenance}</div>
          <div class="stat-label">Perlu perawatan</div>
        </div>
        <div class="stat-card">
          <div class="stat-number" style="color:#dc2626">{damaged}</div>
          <div class="stat-label">Rusak</div>
        </div>
      </div>

      <div class="section-title">Legenda kondisi aset</div>
      <div class="condition-row">
        <span class="dot" style="background:#16a34a"></span>Baik
      </div>
      <div class="condition-row">
        <span class="dot" style="background:#f59e0b"></span>Perlu Perawatan
      </div>
      <div class="condition-row">
        <span class="dot" style="background:#dc2626"></span>Rusak
      </div>

      <div class="section-title">Jumlah menurut kategori</div>
      {bars}

      <div class="dashboard-note">
        Gunakan kontrol layer di kanan atas peta untuk
        memilih kelompok kategori dan kondisi.
        Klik penanda untuk melihat detail aset.<br><br>
        Data contoh bersifat dummy/ilustratif.
      </div>
    </div>
    """

    asset_map.get_root().html.add_child(
        folium.Element(dashboard_html)
    )


def create_interactive_map(df: DataFrame, output_file: Path) -> None:
    """Membuat peta jalan dengan layer yang bisa diaktifkan."""
    center = [
        float(df["latitude"].mean()),
        float(df["longitude"].mean()),
    ]

    asset_map = folium.Map(
        location=center,
        zoom_start=13,
        tiles=None,
        control_scale=True,
        prefer_canvas=True,
    )

    # Tile standar. Buka HTML melalui server lokal, bukan file://.
    folium.TileLayer(
        tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr='© <a href="https://www.openstreetmap.org/copyright">'
             'OpenStreetMap contributors</a>',
        name="OpenStreetMap",
        overlay=False,
        control=True,
        show=True,
    ).add_to(asset_map)

    # Satu layer untuk setiap kombinasi kategori dan kondisi.
    for category in sorted(df["kategori"].unique()):
        for condition in sorted(df["kondisi"].unique()):
            subset = df[
                (df["kategori"] == category)
                & (df["kondisi"] == condition)
            ]

            if subset.empty:
                continue

            layer_name = (
                f"{escape(str(category))} — {escape(str(condition))}"
            )
            group = folium.FeatureGroup(
                name=layer_name,
                show=True,
            )

            color = CONDITION_COLORS.get(condition, DEFAULT_COLOR)

            for _, row in subset.iterrows():
                popup_html = f"""
                <div style="font-family:Arial,sans-serif;min-width:190px">
                  <h4 style="margin:0 0 10px">
                    {escape(str(row['nama_aset']))}
                  </h4>
                  <b>ID aset:</b> {escape(str(row['id_aset']))}<br>
                  <b>Kategori:</b> {escape(str(row['kategori']))}<br>
                  <b>Kondisi:</b>
                  <span style="color:{color};font-weight:bold">
                    {escape(str(row['kondisi']))}
                  </span><br>
                  <b>Latitude:</b> {row['latitude']}<br>
                  <b>Longitude:</b> {row['longitude']}
                </div>
                """

                folium.CircleMarker(
                    location=[
                        float(row["latitude"]),
                        float(row["longitude"]),
                    ],
                    radius=8,
                    color="#ffffff",
                    weight=2,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.95,
                    tooltip=escape(str(row["nama_aset"])),
                    popup=folium.Popup(popup_html, max_width=320),
                ).add_to(group)

            group.add_to(asset_map)

    # Sesuaikan zoom dengan seluruh titik aset.
    bounds = [
        [float(df["latitude"].min()), float(df["longitude"].min())],
        [float(df["latitude"].max()), float(df["longitude"].max())],
    ]
    asset_map.fit_bounds(bounds, padding=(35, 35))

    folium.LayerControl(collapsed=True).add_to(asset_map)
    add_dashboard_panel(asset_map, df)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    asset_map.save(str(output_file))


def save_summaries(df: DataFrame, output_dir: Path) -> None:
    """Menyimpan ringkasan kategori dan kondisi ke CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)

    df.groupby("kategori").size().reset_index(
        name="jumlah_aset"
    ).to_csv(
        output_dir / "ringkasan_kategori.csv",
        index=False,
        encoding="utf-8-sig",
    )

    df.groupby("kondisi").size().reset_index(
        name="jumlah_aset"
    ).to_csv(
        output_dir / "ringkasan_kondisi.csv",
        index=False,
        encoding="utf-8-sig",
    )


def main() -> int:
    global folium, pd

    try:
        folium = import_module("folium")
        pd = import_module("pandas")
    except ModuleNotFoundError as error:
        print(
            f"Dependensi belum terpasang: {error.name}. "
            "Jalankan: python -m pip install folium pandas",
            file=sys.stderr,
        )
        return 1

    try:
        assets = load_and_validate_data(DATA_FILE)
        output_file = OUTPUT_DIR / "peta_aset.html"

        create_interactive_map(assets, output_file)
        save_summaries(assets, OUTPUT_DIR)

        print(f"Berhasil memproses {len(assets)} aset.")
        print(f"Peta dashboard: {output_file}")
        print(f"Ringkasan CSV: {OUTPUT_DIR}")
        print("Catatan: data contoh bersifat dummy/ilustratif.")
        return 0

    except (
        FileNotFoundError,
        ValueError,
        pd.errors.ParserError,
        UnicodeDecodeError,
    ) as error:
        print(f"Terjadi kesalahan: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
