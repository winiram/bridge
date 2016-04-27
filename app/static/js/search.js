
  //////////////////////////// POPULATE HEADERS AND RECORD DATA ////////////////////////////
    $.ajax({
    url: "/getData",
    type: 'get',
    dataType: 'json',
    error: function(data){
      console.log("some error has occured :((((")
    },
    success: function(data){
      console.log(data);
      console.log("succeess")
  var table = [];
  var headers = [];
  var headerRow=[];
  var gridView = [];
  var rowNum =0;

   // <button data-target="m0" class="btn modal-trigger">Modal</button>

  var deetButtonStart =  '<td> <a class="modal-trigger" href="#m'
  var deetButtonEnd = '"><i class="material-icons">zoom_in</i></a></td>'

  modalMaker(data, rowNum);

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

              // gridMaker(table_header, sub_val, gridItem, gridView)
              if(table_header == "media"){
                var gridRow = ' <img src="'+ sub_val + '">'
                gridItem += gridRow;
                continue}
  // HEADERS make headers, put the id as the header name
              headers.push("<th data-field='"+table_header+"'>"+ table_header+"</th>");

  // LIST VIEW make rows for list view and restrict the collumns
             count2.push('x')
             if(count2.length <= 5){

              var record = '<td>' + sub_val + '</td>'
              row.push(record);

  // GRID VIEW make grid items
              var gridRow = '<p><b>'+ table_header + ":</b> " + sub_val + '</p>'
              gridItem += gridRow;
              };
          }
  // LIST & GRID VIEW adds table rows with details button (and row number as ID)
           table.push('<tr>'+ deetButtonStart + rowNum + deetButtonEnd + row +"</tr>")
           gridView.push("<div class= 'col s3 gridItem'>"+ gridItem +"</div>")
           // console.log(rowNum)
           rowNum+=1;

      };
  // HEADERS
      headerRow.push("<th></th>")
     // make headers and restrict their legnth too
        for (i = 0; i < 5; i++) {

          headerRow.push(headers[i])
        }


  $("#table_head").append('<tr>'+ headerRow+'/<tr>')
  $("#table_results").append(table)
  $("#gridView").append(gridView)

  }
  });

  /////////////////////////////////// END POPULATE HEADERS AND RECORD DATA /////////////////////////////////

    // <div id="m0" class="modal modal-fixed-footer">
    //   <div class="modal-content">
    //     <h4>About the Project</h4>
    //     <p>test modal</p>
    //   </div>
    //   <div class="modal-footer">
    //     <a href="#m1" class="modal-action modal-trigger modal-close waves-effect waves-green btn-flat ">next</a>
    //     <a href="#!" class="modal-action modal-close waves-effect waves-green btn-flat ">Close</a>
    //   </div>
    // </div>


  function modalMaker (data, rowNum) {
  var modalStart = '<div id="m' // plus row num
  var modal2_rec = '"class="modal modal-fixed-footer modalContent"><div class="modal-content"><h4>Record Detail</h4>' //plus details
  var modal_close = '<a href="#!" class="modal-action modal-close waves-effect waves-green btn-flat ">Close</a></div></div>'

  var modal_content = [];


     for(i in data){

          var key = i;
          var val = data[i];

          // console.log(content)
          // console.log(rowNum)
          var content= [];

          for(j in val){
              var table_header = j;
              var sub_val = val[j];

              if(table_header == "media"){
                content = content + '</br><img src="'+ sub_val + '">'

                continue}

              content = content + ("<p><b>"+table_header+": </b>"+sub_val+"</p>")

          };

          modal_content.push(modalStart + rowNum + modal2_rec + content +'</div><div class="modal-footer">' + modal_close)
          rowNum +=1;
    };
  $('#insert_modals').append(modal_content);

  };


  // function gridMaker (table_header, sub_val, gridItem, gridView) {
  //   // body...
  // }
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
