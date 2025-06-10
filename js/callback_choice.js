var data = source.data;
var index = -1;
var category = select_category.value;
var selected_gkz = data['selected_gkz'];
var list_of_selected_gkzs = [];
const MAX_SELECTED_ITEMS = 132;
const path_csv = 0;

//Remove previous choices
for (let i = 0; i < selected_gkz.length; i++) {
    if(selected_gkz[i] !== '') list_of_selected_gkzs.push(selected_gkz[i]);
}

if (list_of_selected_gkzs.length > 0) {
    for (let i = 0; i < list_of_selected_gkzs.length; i++) {
        selected_gkz.splice(selected_gkz.indexOf(list_of_selected_gkzs[i]), 1);
        if(selected_gkz.length < MAX_SELECTED_ITEMS){
            selected_gkz.push('');
        }
        data['fill_color'][data['gkz'].indexOf(list_of_selected_gkzs[i])] = "#ffffff";
    }
}

if(category === 'Gemeinde'){
    //Select gemeinde
    index = data['gemeinde'].indexOf(this.value);
    set_gemeinde(index);    
}else {
    /*//Select gemeinden from bezirk xy
    //Remove Umlaute (äöüß)
    const umlautMap = {
        '\u00dc': 'UE',
        '\u00c4': 'AE',
        '\u00d6': 'OE',
        '\u00fc': 'ue',
        '\u00e4': 'ae',
        '\u00f6': 'oe',
        '\u00df': 'ss',
    }
    
    function replaceUmlaute(str){
        return str
            .replace(/[\u00dc|\u00c4|\u00d6][a-z]/g, (a) => {
                const big = umlautMap[a.slice(0, 1)];
                return big.charAt(0) + big.charAt(1).toLowerCase() + a.slice(1);
            })
            .replace(new RegExp('['+Object.keys(umlautMap).join('|')+']', "g"), (a) => umlautMap[a]);
    }
    
    var value_without_Umlaut = replaceUmlaute(this.value);

    //list of bkzs for every bezirk
    var bkzs = {'Klagenfurt Land': '204',
        'Klagenfurt Stadt': '201',
        'Villach Land': '207',
        'Villach Stadt': '202',
        'Hermagor': '203',
        'St.Veit an der Glan': '205',
        'Spittal an der Drau': '206',
        'Voelkermarkt': '208',
        'Wolfsberg': '209',
        'Feldkirchen': '210'
    };

    //Get the bkz numbers from selected bezirk
    var bkzs_nr = bkzs[value_without_Umlaut];
    //Select gemeinden of bezirke xy
    for (let i = 0; i < data['gkz'].length; i++) {
        var gkz = data['gkz'][i];
        if(gkz.substring(0,3) == bkzs_nr){
            set_gemeinde(i);
        }
    }*/

    //Select gemeinden depending on category
    for (let i = 0; i < list_data.length; i++) {
        const element = list_data[i];
        if(element[category] === this.value){
            var index_gkz = data['gkz'].indexOf(element['Gkz'].toString());
            set_gemeinde(index_gkz);
        }
    }
}

//Select gemeinde in map and saved it in selected_gkz list
function set_gemeinde(index){
    if(index != -1){
        data['fill_color'][index] = "#F56D8D";
        selected_gkz.push(data['gkz'][index]);
    } 
}
 
//Save changes
source.change.emit();
source.selected.change.emit();

//Send data to python server
window.parent.stBridges.send('my-bridge', data);