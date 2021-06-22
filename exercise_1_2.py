from datetime import datetime, timedelta
import json
import pprint
import xml.dom.minidom


def set_depart_return_dates(x: int, y: int) -> None:
    """
    Updates DEPARTS and RETURN fields, and writes the result to a new file

    :param x: depart offset in days
    :param y: return offset in days
    :return:  None
    """
    if not x or not y:
        return
    with open("test_payload1.xml") as xml_file:
        tree = xml.dom.minidom.parse(xml_file)
        depart_node = tree.getElementsByTagName("DEPART")
        return_node = tree.getElementsByTagName("RETURN")

        new_depart = datetime.strptime(
            depart_node[0].firstChild.nodeValue, '%Y%m%d') \
            + timedelta(days=x)
        depart_node[0].firstChild.nodeValue = new_depart.strftime('%Y%m%d')

        new_return = datetime.strptime(
            return_node[0].firstChild.nodeValue, '%Y%m%d') \
            + timedelta(days=y)
        return_node[0].firstChild.nodeValue = new_return.strftime('%Y%m%d')

        with open("test_result.xml", "w+") as result_file:
            tree.writexml(result_file)


def remove_json_elem(json_elem: str) -> None:
    """
    Removes a json element from a json file, and writes the result to a new file

    :param json_elem: json element to delete
    :return: None
    """
    if not json_elem:
        return
    with open("test_payload.json") as json_file:
        content = json.load(json_file)
        for k, v in list(content.items()):
            if k == json_elem:
                del content[k]
                break
            if isinstance(v, dict):
                for i in list(v.keys()):
                    if i == json_elem:
                        del v[i]
                        break
        pprint.pprint(content)
        with open("test_result.json", "w+") as result_file:
            result_file.write(json.dumps(content, indent=4))


if __name__ == "__main__":
    remove_json_elem("appdate")
    # remove_json_elem("outParams")
    set_depart_return_dates(6, 9)
