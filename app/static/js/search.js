//////////////////////////// POPULATE HEADERS AND RECORD DATA ////////////////////////////

  $.ajax({
  url: '../static/databaseCache.json',
  type: 'get',
  dataType: 'json',
  error: function(data){
    console.log("some error has occured :((((")
    
  },
  success: function(data){
    console.log("succeess")
var table = [];
var headers = [];
var headerRow=[];
var gridView = [];
var rowNum =0;

 // <button data-target="m0" class="btn modal-trigger">Modal</button>

var deetButtonStart =  '<td> <a class="waves-effect waves-light btn modal-trigger" href="#'
var deetButtonEnd = '">Q</a></td>'


    for(i in data){

        var key = i;
        var val = data[i];
        var row = [];
        var gridItem = " ";

// column count!
        var count = []
        for(i in val){
          count.push('x')
        }

 // make rows (list and grid views)
  var count2 = []
        for(j in val){

// get values
            var table_header = j;
            var sub_val = val[j];
        
            if(table_header == "imglink"){
              var gridRow = ' <img src="'+ sub_val + '">'
              gridItem += gridRow;
              continue}
// make headers, put the id as the header name
            headers.push("<th data-field='"+table_header+"'>"+ table_header+"</th>");             
// make rows for list view and restrict the collumns
           count2.push('x')
           if(count2.length <= 5){

            var record = '<td>' + sub_val + '</td>'   
            row.push(record);
          
// make grid items
            var gridRow = '<p><b>'+ table_header + ":</b> " + sub_val + '</p>'
            gridItem += gridRow;   
            };
        }
// adds table rows with details button (and row number as ID)
         table.push('<tr>'+ deetButtonStart + rowNum + deetButtonEnd + row +"</tr>")
         gridView.push("<div class= 'col s3 gridItem'>"+ gridItem +"</div>")
         // console.log(rowNum)
         rowNum+=1;

    };
    headerRow.push("<th></th>")
   // make headers and restrict their legnth too
      for (i = 0; i < 5; i++) { 

        headerRow.push(headers[i])
      }
      

$("#table_head").append('<tr>'+ headerRow+'/<tr>')
$("#table_results").append(table)
$("#gridView").append(gridView)
// $("#0").click(function(){
//   alert("hiii");
// });






}
});

/////////////////////////////////// END POPULATE HEADERS AND RECORD DATA /////////////////////////////////


function deets(q){
  // console.log(q.id)

  $.ajax({
  url: '../static/databaseCache.json',
  type: 'get',
  dataType: 'json',
  error: function(data){
    console.log("an error getting the record has occured")
    
  },
  success: function(data){
    console.log("got the data")


  for(i in data){
        var key = q.id;
        if(Number(i)===Number(key)){
          console.log(key)
        var val = data[i];
        console.log(val)




        // for(j in val){

        // // get values
        //             var table_header = j;
        //             var sub_val = val[j];
                
        //             if(table_header == "imglink"){
        //               var gridRow = ' <img src="'+ sub_val + '">'
        //               gridItem += gridRow;
        //               continue}





        }
      }
    }
  }
  )};


/////////////////////////// SEARCH FIELDS ////////////////////////////////////////////////////////
$(function() {
      $(".clearbtn").click( function()
           { console.log("clear button is clicked!")
           $(this).closest('form').find("input[type=text], textarea").val("");


           }
      );
});

$(function() {
      $(".searchbtn").click( function()
           { console.log("search button is clicked!")
           // gets all form data
           $( ".searchItem" ).each(function( index ) {
             var queryStr = $(this).val();
 
              console.log(queryStr);


            });

           // for each search item given, look in the designated search fields in the DB.  hide all others.

           }
      );
});