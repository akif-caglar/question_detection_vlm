import re
from PIL import Image

def map_coordinates(small_docling_coords, small_width, small_height, original_width, original_height):
    scale_x = original_width / small_width
    scale_y = original_height / small_height
    
    original_coords = [(int(x * scale_x), int(y * scale_y)) for x, y in small_docling_coords]
    return original_coords

def is_digit_text(line):
    text = line.replace("<", ">")
    text = text.split(">")
    
    for el in text:
        if el.isdigit():
            return True
    
    return False

def parse_lines(text):
    lines = text.split("\n")
    parsed_lines = []
    
    for line in lines:
        if line == "":
            continue
        parsed_lines.append(line)
    
    return parsed_lines

def find_question_lines(lines):
    bounding_boxes = []
    for d_index, line in enumerate(lines):
        if "D)" in line:
            collected_lines = [line]
            
            for i in range(d_index - 1, -1, -1):
                if "picture" in lines[i]:
                    break
                elif is_digit_text(lines[i]):
                    collected_lines.append(lines[i])
                    break
                else:
                    collected_lines.append(lines[i])
            
            collected_lines.reverse()
            bounding_boxes.append(collected_lines)
    
    return bounding_boxes

def extract_bb_from_line(doctag_lines):
    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')
    
    for line in doctag_lines:
        locs = list(map(int, re.findall(r'\d+', line)))
        if is_digit_text(line):
            locs[1] = locs[3] + 5
            locs[3] = locs[3] + 5
        if len(locs) > 3:
            locs = locs[0:4]
            x1, y1, x2, y2 = locs
            min_x = min(min_x, x1, x2)
            min_y = min(min_y, y1, y2)
            max_x = max(max_x, x1, x2)
            max_y = max(max_y, y1, y2)
    
    return (min_x, min_y, max_x, max_y)

def crop_questions(image, boxes):
    merged_boxes = []
    questions = []
    for box in boxes:
        int_box = extract_bb_from_line(box)
        merged_boxes.append(int_box)
    original_width, original_height = image.size

    for box1 in merged_boxes:
        x1, y1, x2, y2 = box1[0], box1[1], box1[2], box1[3]
        small_docling_coords = [(x1, y1), (x2, y2)]
        small_width, small_height = 500, 500 #smallDocling layout resolution
        mapped_coords = map_coordinates(small_docling_coords, small_width, small_height, original_width, original_height)
        print("Mapped Coordinates:", mapped_coords)
        crop = mapped_coords
        cropped = image.crop((crop[0][0],crop[0][1],crop[1][0],crop[1][1]))
        questions.append(cropped)
    return questions

def concatenate_imgs(images):
    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)
    new_image = Image.new("RGB", (total_width, max_height))
    x_offset = 0
    for img in images:
        new_image.paste(img, (x_offset, 0))
        x_offset += img.width
    return new_image