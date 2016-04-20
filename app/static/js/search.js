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
    // console.log(data.length)

var table = [];
var headers = [];
var headerRow=[];
var gridView = [];

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
        for(j in val){
// get values
            var table_header = j;
            var sub_val = val[j];
        
            if(table_header == "imglink"){
              console.log("img!!")
              continue}
// make headers, put the id as the header name
            headers.push("<th data-field='"+table_header+"'>"+ table_header+"</th>");             
// make rows for list view
            var record = '<td>' + sub_val + '</td>'   
            row.push(record);
// make grid items
            var gridRow = '<p>'+ table_header + ": " + sub_val + '</p>'
            gridItem += gridRow;   
        }
         table.push("<tr>"+row+"</tr>")
         gridView.push("<div class= 'col s3 gridItem'>"+ gridItem +"</div>")
         
      }
   // make headers

            
      for (i = 0; i < count.length-1; i++) { 


        headerRow.push(headers[i])
      }

$("#table_head").append('<tr>'+ headerRow+'/<tr>')
$("#table_results").append(table)
$("#gridView").append(gridView)

}
});

/////////////////////////////////// END POPULATE HEADERS AND RECORD DATA /////////////////////////////////


$(document).ready(function() {
    $('<rect>').click(function(e) {  
      alert(1);
    });
});

/////////////////////////// SEARCH FIELDS ////////////////////////////////////////////////////////
$(function() {
      $("#clearbtn").click( function()
           { console.log("clear button is clicked!")

           // $( ".searchItem" ).each(function( index ) {
           //   var queryStr = $(this).val();
 
           //    console.log(queryStr);

           //  });


           }
      );
});

$(function() {
      $("#searchbtn").click( function()
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