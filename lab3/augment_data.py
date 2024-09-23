import pandas as pd
from PIL import Image

mask_dir = './masks/'
image_dir = './images/'

def rotate_image(image, mask, img_name, mask_name, type, rotations, data_dict):
    for rot in rotations:
        rotated_image = image.rotate(rot)
        rotated_mask = mask.rotate(rot)

        new_image_name = f"{img_name}_rot{rot}.png"
        new_mask_name = f"{mask_name}_rot{rot}.png"

        new_data['idx'].append(row['idx'] * rot)
        new_data['image_file'].append(new_image_name)
        new_data['mask_file'].append(new_mask_name)
        new_data['type'].append(type)

        rotated_image.save(image_dir + new_image_name)
        rotated_mask.save(mask_dir + new_mask_name)

df = pd.read_csv('./data.csv')

new_data = {
    'idx': [],
    'image_file': [],
    'mask_file': [],
    'type': [],
}

rotations = [30, 45, 60, 90, 330, 315, 300, 270, 180]
for i, row in df.iterrows():
    print(f"\rImage {i} - {row['image_file']}")
    original_image = Image.open(image_dir + row['image_file']).resize((512, 512))
    original_mask = Image.open(mask_dir + row['mask_file']).resize((512, 512))

    original_image_name = row['image_file'][:-4]
    original_mask_name = row['mask_file'][:-4]

    vert_flip_image = original_image.transpose(Image.FLIP_TOP_BOTTOM)
    vert_flip_mask = original_mask.transpose(Image.FLIP_TOP_BOTTOM)
    vert_flip_img_name = f"{original_image_name}_vflip"
    vert_flip_mask_name = f"{original_mask_name}_vflip"

    hor_flip_image = original_image.transpose(Image.FLIP_LEFT_RIGHT)
    hor_flip_mask = original_mask.transpose(Image.FLIP_LEFT_RIGHT)
    hor_flip_img_name = f"{original_image_name}_hflip"
    hor_flip_mask_name = f"{original_mask_name}_hflip"

    new_data['idx'].append(row['idx'] * 11)
    new_data['image_file'].append(vert_flip_img_name + '.png')
    new_data['mask_file'].append(vert_flip_mask_name + '.png')
    new_data['type'].append(row['type'])

    vert_flip_image.save(image_dir + vert_flip_img_name + '.png')
    vert_flip_mask.save(mask_dir + vert_flip_mask_name + '.png')

    new_data['idx'].append(row['idx'] * 12)
    new_data['image_file'].append(hor_flip_img_name + '.png')
    new_data['mask_file'].append(hor_flip_mask_name + '.png')
    new_data['type'].append(row['type'])

    hor_flip_image.save(image_dir + hor_flip_img_name + '.png')
    hor_flip_mask.save(mask_dir + hor_flip_mask_name + '.png')

    rotate_image(original_image, original_mask, original_image_name, original_mask_name, row['type'], rotations, new_data)
    rotate_image(hor_flip_image, hor_flip_mask, hor_flip_img_name, hor_flip_mask_name, row['type'], rotations, new_data)
    rotate_image(vert_flip_image, vert_flip_mask, vert_flip_img_name, vert_flip_mask_name, row['type'], rotations, new_data)


print("")
new_df = pd.DataFrame.from_dict(new_data)
merged_df = pd.concat([df, new_df])
print(merged_df)
merged_df.to_csv('./data.csv')