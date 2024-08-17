def get_class_by_name(name, class_list):
    return next((cls for cls in class_list if cls.__name__ == name), None)
