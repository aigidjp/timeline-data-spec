import geopandas as gpd
import pandas as pd
import pyproj
from shapely import wkt


def main():
    timeline_data = pd.read_csv(
        "./sample_data/timeline_data.csv",
        delimiter=",",
        names=[
            "id",
            "00:00",
            "01:00",
            "02:00",
            "03:00",
            "04:00",
            "05:00",
            "06:00",
            "07:00",
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
            "18:00",
            "19:00",
            "20:00",
            "21:00",
            "22:00",
            "23:00",
        ],
        dtype={
            "id": int,
            "00:00": str,
            "01:00": str,
            "02:00": str,
            "03:00": str,
            "04:00": str,
            "05:00": str,
            "06:00": str,
            "07:00": str,
            "08:00": str,
            "09:00": str,
            "10:00": str,
            "11:00": str,
            "12:00": str,
            "13:00": str,
            "14:00": str,
            "15:00": str,
            "16:00": str,
            "17:00": str,
            "18:00": str,
            "19:00": str,
            "20:00": str,
            "21:00": str,
            "22:00": str,
            "23:00": str,
        },
    )

    features = pd.read_csv(
        "./sample_data/features.tsv",
        delimiter="\t",
        names=[
            "id",
            "name",
            "wkt",
        ],
        dtype={"id": int, "name": str, "wkt": str},
    )

    columns = [
        "00:00",
        "01:00",
        "02:00",
        "03:00",
        "04:00",
        "05:00",
        "06:00",
        "07:00",
        "08:00",
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00",
        "20:00",
        "21:00",
        "22:00",
        "23:00",
    ]

    timeline_data["timeline_data"] = timeline_data[columns].apply(", ".join, axis=1)
    timeline_data = timeline_data.drop(columns=columns)

    merged = pd.merge(features, timeline_data, how="inner", on="id").set_index("id")

    merged["geometry"] = merged.wkt.apply(wkt.loads)

    merged = gpd.GeoDataFrame(merged)
    merged = merged.drop("wkt", axis=1)
    merged = merged.set_crs(pyproj.CRS(4326))
    merged.to_file("./sample_data/output.geojson", driver="GeoJSON")

    # MVTに変換するには以下のようなコマンドを実行
    # "tippecanoe -e ./sample_data/output -pf -pk -pC -Z 10 -z 14 -f ./sample_data/output.geojson"


if __name__ == '__main__':
    main()
