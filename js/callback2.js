var selected_indices = source.selected.indices;
var data = source.data;
var selected_gkz = data['selected_gkz'];
var gkz = data['gkz'];

// Iterate over selected indices
for (var i = 0; i < selected_indices.length; i++) {
    var index = selected_indices[i];
    var list_of_selected_gkzs = gkz[index];
    const MAX_SELECTED_ITEMS = 132;
    
    // Toggle the selection status
    if (selected_gkz.includes(list_of_selected_gkzs)) {
        //unselected
        // If already selected, remove it
        selected_gkz.splice(selected_gkz.indexOf(list_of_selected_gkzs), 1);
        if(selected_gkz.length < MAX_SELECTED_ITEMS){
            selected_gkz.push('');
        }
        data['fill_color'][index] = "#ffffff"; // Reset to blue
        console.log("unselected:", list_of_selected_gkzs);
    } else {
        //selected
        // If not selected, add it
        
        selected_gkz.push(list_of_selected_gkzs);
        if(selected_gkz.length >= MAX_SELECTED_ITEMS){
            selected_gkz.shift();
        }
        data['fill_color'][index] = "#F56D8D"; // Set to red
        console.log("selected:", list_of_selected_gkzs);
    }
    //var selected_gkz = [];
   // function updateSelectedGkz(gkz, selected){
     //   var index = selected_gkz.indexOf(gkz);
       // if(selected && index === -1){
         //   selected_gkz.push(gkz);
        //}else if(!selected && index !== -1){
          //      selected_gkz.splice(index, 1);
            //}
        //}

    /*source.selected.js_on_change('indices', function(cb_obj){
        var indices = cb_obj.indices;
        var data = source.data;
        selected_gkz = [];
        for(var i = 0; i < data['gkz'].length;i++){
        //var gkz= data['gkz'][i];
        //var selected = indices.includes(i);
        //updateSelectedGkz(gkz, selected);
            if(indices.includes(i)){
                selected_gkz.push(data['gkz'][i])
            }
        }
        console.log("Selected GKZs: ", selected_gkz);
        Streamlit.setComponentValue(selected_gkz);
    });*/
}
 // Define global variable to store selected GKZs (outside of CustomJS function)
var gkzSelection = [];

// ... inside CustomJS function
source.selected.indices.forEach(idx => {
    let selectedGKZ = source.data['gkz'][idx] // get selected GKZ from map data source
  
    if (selectedGKZ != null && !gkzSelection.includes(selectedGKZ)) {
        gkzSelection.push(selectedGKZ);
    }
});

for(let j=0;j<selected_gkz.length;j++){
    if(selected_gkz[j] != '')    
        console.log("GKZ: " + selected_gkz[j]);
}

//console.log('Selected GKZ: ', selected_indices)
// Update the data source
source.data = data;
source.change.emit();
source.selected.change.emit();

//Send Data to Streamlit(Python) (Ref: https://discuss.streamlit.io/t/how-to-send-data-from-javascript-to-streamlit-using-p5js-in-streamlit/75604/2)
window.parent.stBridges.send('my-bridge', data);


/*
function selectList(listName){
    if(listName === 'kaernten'){
        bulkSelect(kaernten_gkz);
    }else if(bezirk_gkz[listName]){
        bulkSelect(bezirk_gkz[listName]);
    }else if(tr_gkz[listName]){
        bulkSelect(tr_gkz[listName]);
    }
}

source2.data2 = data2;
source2.change.emit();
*/
//var kaernten_gkz = [];
//var bezirk_gkz = [];
//var tr_gkz = [];
//var final_gkz = []*132;

/*
//buttons
button_kaernten = Button(label="Kärnten", button_type="success", id="select_kaernten")


// funktion um bulk selection zu handeln
function bulkSelect(gkz){
    gkzList.forEach((current_gkz)=>{
        var index = gkz.indexOf(current_gkz);
        if(index > -1){
            if(!selected_gkz.includes (current_gkz)){
                selected_gkz.push(current_gkz);
                if(selected_gkz.length >=132){
                    selected_gkz.shift();

                }
                data['fill_color'][index] = "ff0000";
            }
        }
    });
}


// Handle individuelle selection
selected_indices.forEach((index)=>{
    var current_gkz = gkz[index];
    const MAX_SELECTED_ITEMS = 132;
    if(selected_gkz.includes(current_gkz)){
        selected_gkz.splice(selected_gkz.indexOf(current_gkz),1);
        if(selected_gkz.length < MAX_SELECTED_ITEMS){
            selected_gkz.push('');
        }
        data['fill_color'][index] = "#d2b48c";
        console.log("unselected");
    }else{
        selected_gkz.push(current_gkz);
        if(selected_gkz.length >= MAX_SELECTED_ITEMS){
            selected_gkz.shift();
        }
        data['fill_color'][index] = '#ff0000';
        console.log('selected');
    }
});
*/