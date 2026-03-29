import json

def fix_chinese_place_names(input_filepath, output_filepath):
    """
    读取 GeoJSON 文件，更正中文地名翻译，并保存为新文件。
    """
    # 1. 读取原始 GeoJSON 文件
    try:
        with open(input_filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"找不到文件: {input_filepath}，请确保文件路径正确。")
        return

    # 2. 定义替换规则字典 (可以自由添加或修改)
    # 格式为: {"旧文本": "新文本"}
    replace_rules = {
        "北西": "西北",
        "南西": "西南",
        "北东": "东北",
        "南东": "东南",
        "东方": "东部",
        "西方": "西部",
        "南方": "南部",
        "北方": "北部",
        "地方": "地区",
        "冲": "海域"
    }

    # 需要处理的语言字段 (简体中文和繁体中文)
    target_keys = ["name_zh-cn", "name_zh-tw"]
    
    modified_count = 0

    # 3. 遍历并修改数据
    for feature in data.get("features", []):
        properties = feature.get("properties", {})
        
        for key in target_keys:
            if key in properties and isinstance(properties[key], str):
                original_name = properties[key]
                new_name = original_name
                
                # 应用所有替换规则
                for old_text, new_text in replace_rules.items():
                    new_name = new_name.replace(old_text, new_text)
                
                # 如果名称发生了改变，则更新字典并计数
                if new_name != original_name:
                    properties[key] = new_name
                    modified_count += 1

    # 4. 保存为新的 GeoJSON 文件
    with open(output_filepath, 'w', encoding='utf-8') as file:
        # ensure_ascii=False 保证输出的是真正的中文而不是 Unicode 转义字符
        # indent=2 让输出的 JSON 文件有良好的缩进，方便阅读
        json.dump(data, file, ensure_ascii=False, indent=2)
        
    print(f"处理完成！共修改了 {modified_count} 处地名翻译。")
    print(f"已保存至: {output_filepath}")

# 执行脚本
if __name__ == "__main__":
    # 输入文件名 (请确保该文件与脚本在同一目录下)
    INPUT_FILE = "震央地名.geojson"
    # 输出文件名
    OUTPUT_FILE = "震央地名_修正.geojson"
    
    fix_chinese_place_names(INPUT_FILE, OUTPUT_FILE)