var scatter_data = (function() {   

    g_data = [];
    
    
    function scatter_mouseover(event) {     
        var cursor_x = event.offsetX;
        var cursor_y = event.offsetY;
        
        details_out = ""
        for(ix in g_data) {
            var item = g_data[ix];
            diff_x = item.x - cursor_x;
            diff_y = item.y - cursor_y;
            
            dist = Math.sqrt(diff_x*diff_x + diff_y*diff_y);
            
            if( dist < 10 ) {
                console.log(item.label);
                document.getElementById(item.id).setAttribute('r',10);
                details_out += item.label + "<br>";
            }
            else {
                document.getElementById(item.id).setAttribute('r',2);
            }
        }
        
        document.getElementById("details_div").innerHTML = details_out;     
    };
    
    function load_data(data) {       
        g_data = JSON.parse(data);
        
        console.log("loaded");
        console.log(g_data);
    }
    
    
    return {"scatter_mouseover": scatter_mouseover, "load_data": load_data };
})();



