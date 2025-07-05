import argparse
import subprocess

# Category to synset mapping
object2synset = {
    'chair': '03001627',
    'display': '03211117',
    'table': '04379243',
    "trashbin": "02747177",
    "toolbox": "02773838",
    "monitor": "03211117",
    "keyboard": "03085013",

    # objaverse
    "stool": "stool",
    "boxlarge": "box",
    "boxlong": "box",
    "boxtiny": "box",
    "boxsmall": "box",
    "suitcase": "suitcase",
    "yogaball": "ball",
    "box": "box",
    "ball": "ball",
    "bottle": ["02876657", "02946921"],
    "cup": ["03797390", "02880940"],
    "skateboard": "04225987",
    "plasticcontainer": "02801938",

    # ABO / Objaverse extended
    "abo-chair": 'abo-chair',
    'abo-table': 'abo-table',
    "obja-chair": "obja-chair"
}

# Determine source from category
def infer_source(category: str) -> str:
    shapenet = {'chair', 'display', 'table', 'trashbin', 'toolbox', 'monitor', 'keyboard'}
    objaverse = {'stool', 'boxlarge', 'boxlong', 'boxtiny', 'boxsmall', 'suitcase',
                 'yogaball', 'box', 'ball', 'bottle', 'cup', 'skateboard', 'plasticcontainer'}
    abo = {'abo-chair', 'abo-table', 'obja-chair'}

    if category in shapenet:
        return 'shapenet'
    elif category in objaverse:
        return 'objaverse'
    elif category in abo:
        return 'abo'
    else:
        raise ValueError(f"[ERROR] Unknown category '{category}' – please check spelling or extend the list.")

def get_args():
    parser = argparse.ArgumentParser(description="Render ProciGen object interaction with minimal config")
    parser.add_argument('--object', required=True, help="Object name, e.g. 'stool'")
    parser.add_argument('--category', required=True, help=(
        "Object category (used to infer dataset):\n"
        "ShapeNet: chair, display, table, trashbin, toolbox, monitor, keyboard\n"
        "Objaverse: stool, boxlarge, boxlong, boxtiny, boxsmall, suitcase,\n"
        "           yogaball, box, ball, bottle, cup, skateboard, plasticcontainer\n"
        "ABO/Extended: abo-chair, abo-table, obja-chair"
    ))
    return parser.parse_args()

def main():
    args = get_args()
    obj_name = args.object
    category = args.category.lower()

    source = infer_source(category)

    print(f"[INFO] Running render pipeline")
    print(f"  Object Name : {obj_name}")
    print(f"  Category    : {category}")
    print(f"  Source      : {source}")

    synz_cmd = [
        "python", "synz/synz_batch.py",
        "--seqs_pattern", f"Date01_Sub01*{obj_name}*",
        "--source", source,
        "--object", obj_name,
        "--object_category", category,
        "--outfolder", f"outputs/params/{obj_name}",
        "--batch_size", "16",
        "--iterations", "500",
        "--end", "16"
    ]

    render_cmd = [
        "python", "render/render_hoi.py",
        "-p", f"outputs/params/{obj_name}",
        "--source", source,
        "--obj_name", obj_name,
        "-o", "outputs/render_with_texture"
    ]

    subprocess.run(synz_cmd)
    subprocess.run(render_cmd)

if __name__ == "__main__":
    main()
