"""
Verify Setup - Run This BEFORE Trying to Start the App
------------------------------------------------------------
This checks that all 9 required files exist in the current folder AND
that they're all consistent with each other (same 30 foods, no mismatches
from old versions). Run this FIRST, every time, before "streamlit run app.py".

Run it like: python verify_setup.py
"""

import os
import sys

EXPECTED_FOODS = sorted([
    "apple", "avocado", "banana", "blueberry", "bread", "cabbage", "carrot",
    "cauliflower", "cherry", "corn", "cucumber", "dairy", "egg", "eggplant",
    "grape", "kiwi", "lemon", "mango", "meat", "onion", "orange", "peach",
    "pear", "pepper", "pineapple", "potato", "seafood", "strawberry",
    "tomato", "watermelon",
])

REQUIRED_FILES = [
    "food_model.keras",
    "class_names.txt",
    "freshness_model_v2.keras",
    "freshness_v2_class_names.txt",
    "expiry_model.joblib",
    "food_encoder.joblib",
    "storage_encoder.joblib",
    "status_encoder.joblib",
    "recipe_lookup.json",
    "app.py",
    "requirements.txt",
]

errors = []
warnings = []

print("=" * 60)
print("STEP 1: Checking all files exist")
print("=" * 60)
for filename in REQUIRED_FILES:
    if os.path.exists(filename):
        print(f"  [OK] {filename}")
    else:
        print(f"  [MISSING] {filename}")
        errors.append(f"Missing file: {filename}")

if errors:
    print("\nSTOP - fix missing files before continuing. Not checking further.")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("STEP 2: Checking class_names.txt matches the expected 30 foods")
print("=" * 60)
with open("class_names.txt") as f:
    class_names = sorted([line.strip() for line in f.readlines() if line.strip()])

if class_names == EXPECTED_FOODS:
    print(f"  [OK] class_names.txt has exactly the right 30 foods")
else:
    print(f"  [MISMATCH] class_names.txt does NOT match expected foods")
    print(f"  Found {len(class_names)} foods: {class_names}")
    missing = set(EXPECTED_FOODS) - set(class_names)
    extra = set(class_names) - set(EXPECTED_FOODS)
    if missing:
        print(f"  Missing: {sorted(missing)}")
    if extra:
        print(f"  Unexpected extra: {sorted(extra)}")
    errors.append("class_names.txt mismatch")

print("\n" + "=" * 60)
print("STEP 3: Checking food_model.keras matches class_names.txt")
print("=" * 60)
try:
    import tensorflow as tf
    model = tf.keras.models.load_model("food_model.keras")
    model_classes = model.output_shape[-1]
    if model_classes == len(class_names):
        print(f"  [OK] food_model.keras expects {model_classes} classes, matches class_names.txt")
    else:
        print(f"  [MISMATCH] food_model.keras expects {model_classes} classes, but class_names.txt has {len(class_names)}")
        errors.append("food_model.keras / class_names.txt count mismatch")
except Exception as e:
    print(f"  [ERROR] Could not load food_model.keras: {e}")
    errors.append(f"food_model.keras failed to load: {e}")

print("\n" + "=" * 60)
print("STEP 4: Checking expiry_model's food_encoder matches class_names.txt")
print("=" * 60)
try:
    import joblib
    food_encoder = joblib.load("food_encoder.joblib")
    encoder_foods = sorted(food_encoder.classes_)
    if encoder_foods == EXPECTED_FOODS:
        print(f"  [OK] food_encoder.joblib has exactly the right 30 foods")
    else:
        print(f"  [MISMATCH] food_encoder.joblib does NOT match expected foods")
        print(f"  Found {len(encoder_foods)} foods: {encoder_foods}")
        errors.append("food_encoder.joblib mismatch")
except Exception as e:
    print(f"  [ERROR] Could not load food_encoder.joblib: {e}")
    errors.append(f"food_encoder.joblib failed to load: {e}")

print("\n" + "=" * 60)
print("STEP 4.5: Checking freshness_model_v2 has the expected binary classes")
print("=" * 60)
try:
    with open("freshness_v2_class_names.txt") as f:
        freshness_classes = sorted([line.strip() for line in f.readlines() if line.strip()])
    if freshness_classes == ["fresh", "not_fresh"]:
        print(f"  [OK] freshness_v2_class_names.txt has the expected binary classes")
    else:
        print(f"  [MISMATCH] Expected ['fresh', 'not_fresh'], found {freshness_classes}")
        errors.append("freshness_v2_class_names.txt mismatch")

    freshness_model = tf.keras.models.load_model("freshness_model_v2.keras")
    fm_classes = freshness_model.output_shape[-1]
    if fm_classes == len(freshness_classes):
        print(f"  [OK] freshness_model_v2.keras expects {fm_classes} classes, matches")
    else:
        print(f"  [MISMATCH] freshness_model_v2.keras expects {fm_classes}, but file has {len(freshness_classes)}")
        errors.append("freshness_model_v2.keras / class names count mismatch")
except Exception as e:
    print(f"  [ERROR] Could not verify freshness model: {e}")
    errors.append(f"freshness_model_v2 check failed: {e}")

print("\n" + "=" * 60)
print("STEP 5: Checking recipe_lookup.json covers the expected foods")
print("=" * 60)
try:
    import json
    with open("recipe_lookup.json") as f:
        recipe_lookup = json.load(f)
    recipe_foods = sorted(recipe_lookup.keys())
    if recipe_foods == EXPECTED_FOODS:
        print(f"  [OK] recipe_lookup.json covers all 30 expected foods")
    else:
        print(f"  [MISMATCH] recipe_lookup.json food list doesn't match")
        errors.append("recipe_lookup.json food list mismatch")

    empty_foods = [f for f, recipes in recipe_lookup.items() if len(recipes) == 0]
    if empty_foods:
        print(f"  [WARNING] These foods have ZERO recipes: {empty_foods}")
        warnings.append(f"No recipes for: {empty_foods}")
    else:
        print(f"  [OK] every food has at least 1 recipe")

    # Check for non-English text (the Malayalam bug from before)
    non_english_found = []
    for food, recipes in recipe_lookup.items():
        for r in recipes:
            title = r.get("name", "")
            ascii_ratio = sum(1 for c in title if ord(c) < 128) / max(len(title), 1)
            if ascii_ratio < 0.9:
                non_english_found.append(title)
    if non_english_found:
        print(f"  [WARNING] Possible non-English recipes found: {non_english_found[:5]}")
        warnings.append("Non-English recipes present - rerun build_recipe_lookup.py with the language filter")
    else:
        print(f"  [OK] no non-English recipe titles detected")

except Exception as e:
    print(f"  [ERROR] Could not load recipe_lookup.json: {e}")
    errors.append(f"recipe_lookup.json failed to load: {e}")

print("\n" + "=" * 60)
print("FINAL RESULT")
print("=" * 60)
if errors:
    print(f"\n{len(errors)} ERROR(S) FOUND - DO NOT run the app yet:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("\nALL CHECKS PASSED. Your files are consistent and ready.")
    if warnings:
        print(f"\n{len(warnings)} minor warning(s) (not blocking):")
        for w in warnings:
            print(f"  - {w}")
    print("\nYou can now safely run: python -m streamlit run app.py")
