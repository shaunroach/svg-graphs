import sys
import subprocess
import json

global file_path
file_path = "E:\\workspace\\python_histogram\\temp.html"
global json_path
json_path = "E:\\workspace\\python_histogram\\temp.json"

class HtmlTag:
    def __init__(self, tag):
        self.tag = tag
        self.attributes = []
        self.text = None
        self.children = []


    def print_html(self):
        out_str = "<" + self.tag
        for item in self.attributes:
            out_str += " " + item['key'] + "=" + "\"" + item['value'] + "\""
        
        out_str += ">"
        
        for child in self.children:
            out_str += "\n" + child.print_html()
        
        if( self.text is not None ):
            out_str += "\n" + self.text
        
        out_str += "\n</" + self.tag + ">"
        
        return out_str
        
    def add_attribute(self,key,value):
        self.attributes.append({"key": key, "value": value})


def view_svg(path):
    chrome = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    subprocess.check_call([chrome, 'file://'+path, '--kiosk'])
    print("done")
    
def make_text_tag(x,y,text):
    text_tag = HtmlTag("text")
    text_tag.add_attribute("x",str(x))
    text_tag.add_attribute("y",str(y))
    text_tag.text = text
    return text_tag
    
def make_rect_tag(x,y,width,height):
    rect_tag = HtmlTag("rect")
    rect_tag.add_attribute("x",str(x))
    rect_tag.add_attribute("y",str(y))
    rect_tag.add_attribute("width", str(width))
    rect_tag.add_attribute("height", str(height))
    return rect_tag
    
def make_circ_tag(cx,cy,r):
    circ_tag = HtmlTag("circle")
    circ_tag.add_attribute("cx",str(cx))
    circ_tag.add_attribute("cy",str(cy))
    circ_tag.add_attribute("r",str(r))
    circ_tag.add_attribute("stroke","black")
    return circ_tag
    
def make_line_tag(x1,x2,y1,y2):
    line_tag = HtmlTag("line")
    line_tag.add_attribute("x1",str(x1))
    line_tag.add_attribute("x2", str(x2))
    line_tag.add_attribute("y1", str(y1))
    line_tag.add_attribute("y2", str(y2))
    return line_tag
    
def make_svg_tag(width, height):
    tag = HtmlTag("svg")
    tag.attributes.append({"key": "xmlns", "value": "http://www.w3.org/2000/svg"})
    tag.attributes.append({"key": "xmlns:xlink", "value": "http://www.w3.org/1999/xlink"})
    tag.add_attribute("style", "width: 100%; height: 400")
    return tag
    
def write_data_to_json(data_arr, json_file_path):
    file_out = file(json_path, "w")
    file_out.write(data_arr)
    file_out.close()
    
def write_and_view_html(html):
    file_out = file(file_path, "w")
    file_out.write(html.print_html())
    file_out.close()
    
    view_svg(file_path)
    
def make_scatterplot(pair_arr, lines):
    for item in pair_arr:
        assert "input" in item
        assert "output" in item
        assert "desc" in item
        
    for item in lines:
        assert "start" in item
        assert "end" in item
        assert "beta" in item
        assert "alpha" in item

    total_width = 400
    total_height = 400
    left_pad = 20
    top_pad = 10
    
    graph_width = total_width - left_pad
    graph_height = total_height - top_pad
    
    svg_tag = make_svg_tag(total_width, total_height)
    vertical_axis = make_line_tag(left_pad,left_pad,top_pad, 310)
    vertical_axis.add_attribute("style", "stroke:rgb(255,0,0);stroke-width:1;")
    #svg_tag.children.append(vertical_axis)
    html = HtmlTag("html")
    #html.add_attribute("onload", "scatter_data.load_data('temp.json');")
    
    head = HtmlTag("head")
    scatter_mouseover = HtmlTag("script")
    scatter_mouseover.add_attribute("src", "E:\workspace\python_histogram\scatterplot_mousover.js")
    
    head.children.append(scatter_mouseover)
    
    html.children.append(head)
    html.children.append(svg_tag)
    
    details = HtmlTag("div")
    details.add_attribute("id", "details_div")
    html.children.append(details)
    
    svg_tag.add_attribute("onmousemove", "scatter_data.scatter_mouseover(event);");
 
    max_one = 0
    min_one = sys.maxsize
    max_two = 0
    min_two = sys.maxsize
    for item in pair_arr:
        max_one = max(max_one, item['input'])
        min_one = min(min_one, item['input'])
        max_two = max(max_two, item['output'])
        min_two = min(min_two, item['output'])
        
    one_width = max_one - min_one
    two_width = max_two - min_two
    
    one_scale = float(graph_width)/one_width
    two_scale = float(graph_height)/two_width
    
    '''
    Draw Dots
    '''
    data = []
    ix = 0
    for item in pair_arr:
        x_coord = (item['input'] - min_one)*one_scale
        y_coord = (item['output'] - min_two)*two_scale
        
        x_coord += left_pad
        y_coord = top_pad + graph_height - y_coord
        point_svg = make_circ_tag(x_coord, y_coord, 2)
        point_svg.add_attribute("style", "fill-opacity: 0.2; stroke-opacity: 0.4; opacity: 0.9;")
        point_svg.add_attribute("id", str(ix))
        svg_tag.children.append(point_svg)
        
        data.append({"x": x_coord, "y": y_coord, "label": item['desc'] + " (" + str(item['input']) + ", " + str(item['output']) + ")", "id": ix})
        
        ix += 1
        
    svg_tag.add_attribute("onload", "scatter_data.load_data('"+json.dumps(data).replace('"','&quot;').replace('\'', '') +"');")
    
    '''
    Draw Lines
    '''
    for item in lines:
        p1_x = (item['start'] - min_one)*one_scale
        p1_y = ((item['start']*item['beta'] + item['alpha']) - min_two) * two_scale
        p2_x = (item['end'] - min_one)*one_scale
        p2_y = ((item['end']*item['beta'] + item['alpha']) - min_two) * two_scale
        
        p1_x += left_pad
        p2_x += left_pad
        p1_y = top_pad + graph_height - p1_y
        p2_y = top_pad + graph_height - p2_y
        
        regression_line = make_line_tag(p1_x,p2_x, p1_y, p2_y)
        regression_line.add_attribute("style", "stroke:rgb(255,0,0);stroke-width:1;")
        svg_tag.children.append(regression_line)
    
    
    write_data_to_json(json.dumps(data), json_path)
    write_and_view_html(html)
    
    
if __name__ == "__main__":
    make_scatterplot([{'input': 30, 'output': 50, 'desc': '1'}, {'input': 20, 'output': 60, 'desc': '2'}, {'input': 23, 'output': 54, 'desc': '4'}], [{'beta': 1, 'alpha': 30, 'start': 20, 'end': 30, 'desc': '3'}])