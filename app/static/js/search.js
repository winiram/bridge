$(document).ready(function(){
    getData();
    $('#unique_searches-0-search').prepend('<option value=""selected></option>')
  });

function getData () {
  console.log("Getting original data");

  //////////////////////////// POPULATE HEADERS AND RECORD DATA ////////////////////////////
    $.ajax({
      url: "/getData",
      type: 'get',
      dataType: 'json',
      error: function(data){
        console.log("error while getting original data")
      },
      success: function(data) {
        displayData(data)
      }
  });
}


function displayData(data) {
      console.log("Displaying data")
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
              headers.push("<th>"+ table_header+"</th>");

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
           gridView.push("<div class= 'item card gridItem'>"+ gridItem +"</div>")
           // console.log(rowNum)
           rowNum+=1;

      };
  // HEADERS
      headerRow.push("<th></th>")
     // make headers and restrict their legnth too
        for (i = 0; i < 5; i++) {

          headerRow.push(headers[i])
        }

  $("#table_head").html(headerRow);
  $("#table_results").html(table);
  $("#gridView").html(gridView);
  $("#num_rec").html("<h5>"+rowNum+" Record(s)</h5>")
  $('.modal-trigger').leanModal();

}



  /////////////////////////////////// END POPULATE HEADERS AND RECORD DATA /////////////////////////////////


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
  $('#insert_modals').html(modal_content);
  $('.modal-trigger').leanModal();

  };


  /////////////////////////// SEARCH FIELDS ////////////////////////////////////////////////////////
$(function() {
      $(".clearbtn").click( function()
           { console.log("clear button is clicked!")
           $(this).closest('form').find("input[type=text], textarea").val("");
           getData();

           }
      );
});

$(function() {
      $(".searchbtn").click( function()
           { console.log("search button is clicked!");
           getUpdatedData();
         }
       )}
);



function getUpdatedData() {
  console.log("Getting updated data");

  //////////////////////////// POPULATE HEADERS AND RECORD DATA ////////////////////////////
  // Collect form data from form

  // Post to /search with form content and receive json file in return
    $.post({
      url: "/search",
      dataType: 'json',
      data: $('#searchform').serialize(),
      error: function(data, textStatus){
        console.log(textStatus);
        console.log(data)
        console.log("error while getting updated data")
      },
      success: function(data) {
        displayData(data)
      }
  });

}

  //////////////////////////// POPULATE HEADERS AND RECORD DATA ////////////////////////////
//     $.ajax({
//     url: "../static/results.json",
//     type: 'get',
//     dataType: 'json',
//     error: function(data){
//       console.log("some error has occured :((((")
//     },
//     success: function(data){
//       console.log("succeess")
//   var tableRES = [];
//   var headersRES = [];
//   var headerRowRES=[];
//   var gridViewRES = [];
//   var rowNumRES =0;



//   var deetButtonStart =  '<td> <a class="modal-trigger" href="#m'
//   var deetButtonEnd = '"><i class="material-icons">zoom_in</i></a></td>'

//   modalMakerRES(data, rowNumRES);

//       for(i in data){

//           var keyRES = i;
//           var valRES = data[i];
//           var rowRES = [];
//           var gridItemRES = " ";

//   // column count!
//           var countRES = []
//           for(i in valRES){
//             countRES.push('x')
//           }

//    // make rows (list and grid views)
//     var count2RES = []
//           for(j in valRES){

//   // get values
//               var table_headerRES = j;
//               var sub_valRES = valRES[j];

//               // gridMaker(table_header, sub_val, gridItem, gridView)
//               if(table_headerRES == "media"){
//                 var gridRowRES = ' <img src="'+ sub_valRES + '">'
//                 gridItemRES += gridRowRES;
//                 continue}
//   // HEADERS make headers, put the id as the header name
//               headersRES.push("<th>"+ table_headerRES+"</th>");

//   // LIST VIEW make rows for list view and restrict the collumns
//              count2RES.push('x')
//              if(count2RES.length <= 5){

//               var recordRES = '<td>' + sub_valRES + '</td>'
//               rowRES.push(recordRES);

//   // GRID VIEW make grid items
//               var gridRowRE = '<p><b>'+ table_headerRES + ":</b> " + sub_valRES + '</p>'
//               gridItemRES += gridRowRES;
//               };
//           }
//   // LIST & GRID VIEW adds table rows with details button (and row number as ID)
//            tableRES.push('<tr>'+ deetButtonStart + rowNumRES + deetButtonEnd + rowRES +"</tr>")
//            gridViewRES.push("<div class= 'col s3 gridItem'>"+ gridItemRES +"</div>")
//            rowNumRES+=1;

//       };
//   // HEADERS
//       headerRowRES.push("<th></th>")
//      // make headers and restrict their legnth too
//         for (i = 0; i < 5; i++) {

//           headerRowRES.push(headersRES[i])
//         }

//   console.log("here")
//   console.log(data)
//   console.log(headerRowRES)
//   $("#table_head").html(headerRowRES);
//   $("#table_results").html(tableRES);
//   // $("#gridView").html(gridViewRES)

//   }
//   });

//              }
//         );
//   });


// function modalMakerRES (data, rowNum) {
//   var modalStart = '<div id="m' // plus row num
//   var modal2_rec = '"class="modal modal-fixed-footer modalContent"><div class="modal-content"><h4>Record Detail</h4>' //plus details
//   var modal_close = '<a href="#!" class="modal-action modal-close waves-effect waves-green btn-flat ">Close</a></div></div>'

//   var modal_content = [];


//      for(i in data){

//           var key = i;
//           var val = data[i];

//           // console.log(content)
//           // console.log(rowNum)
//           var content= [];

//           for(j in val){
//               var table_header = j;
//               var sub_val = val[j];

//               if(table_header == "media"){
//                 content = content + '</br><img src="'+ sub_val + '">'

//                 continue}

//               content = content + ("<p><b>"+table_header+": </b>"+sub_val+"</p>")

//           };

//           modal_content.push(modalStart + rowNum + modal2_rec + content +'</div><div class="modal-footer">' + modal_close)
//           rowNum +=1;
//     };
//   $('#insert_modals').html(modal_content);
//   console.log(modal_content)
//   $.fn.extend({
//     openModal: function(options) {

//       var $body = $('body');
//       var oldWidth = $body.innerWidth();
//       $body.css('overflow', 'hidden');
//       $body.width(oldWidth);

//       var defaults = {
//         opacity: 0.5,
//         in_duration: 350,
//         out_duration: 250,
//         ready: undefined,
//         complete: undefined,
//         dismissible: true,
//         starting_top: '4%'
//       },
//       $modal = $(this);

//       if ($modal.hasClass('open')) {
//         return;
//       }

//       overlayID = _generateID();
//       $overlay = $('<div class="lean-overlay"></div>');
//       lStack = (++_stack);

//       // Store a reference of the overlay
//       $overlay.attr('id', overlayID).css('z-index', 1000 + lStack * 2);
//       $modal.data('overlay-id', overlayID).css('z-index', 1000 + lStack * 2 + 1);
//       $modal.addClass('open');

//       $("body").append($overlay);

//       // Override defaults
//       options = $.extend(defaults, options);

//       if (options.dismissible) {
//         $overlay.click(function() {
//           $modal.closeModal(options);
//         });
//         // Return on ESC
//         $(document).on('keyup.leanModal' + overlayID, function(e) {
//           if (e.keyCode === 27) {   // ESC key
//             $modal.closeModal(options);
//           }
//         });
//       }

//       $modal.find(".modal-close").on('click.close', function(e) {
//         $modal.closeModal(options);
//       });

//       $overlay.css({ display : "block", opacity : 0 });

//       $modal.css({
//         display : "block",
//         opacity: 0
//       });

//       $overlay.velocity({opacity: options.opacity}, {duration: options.in_duration, queue: false, ease: "easeOutCubic"});
//       $modal.data('associated-overlay', $overlay[0]);

//       // Define Bottom Sheet animation
//       if ($modal.hasClass('bottom-sheet')) {
//         $modal.velocity({bottom: "0", opacity: 1}, {
//           duration: options.in_duration,
//           queue: false,
//           ease: "easeOutCubic",
//           // Handle modal ready callback
//           complete: function() {
//             if (typeof(options.ready) === "function") {
//               options.ready();
//             }
//           }
//         });
//       }
//       else {
//         $.Velocity.hook($modal, "scaleX", 0.7);
//         $modal.css({ top: options.starting_top });
//         $modal.velocity({top: "10%", opacity: 1, scaleX: '1'}, {
//           duration: options.in_duration,
//           queue: false,
//           ease: "easeOutCubic",
//           // Handle modal ready callback
//           complete: function() {
//             if (typeof(options.ready) === "function") {
//               options.ready();
//             }
//           }
//         });
//       }


//     }
//   });

//   $.fn.extend({
//     closeModal: function(options) {
//       var defaults = {
//         out_duration: 250,
//         complete: undefined
//       },
//       $modal = $(this),
//       overlayID = $modal.data('overlay-id'),
//       $overlay = $('#' + overlayID);
//       $modal.removeClass('open');

//       options = $.extend(defaults, options);

//       // Enable scrolling
//       $('body').css({
//         overflow: '',
//         width: ''
//       });

//       $modal.find('.modal-close').off('click.close');
//       $(document).off('keyup.leanModal' + overlayID);

//       $overlay.velocity( { opacity: 0}, {duration: options.out_duration, queue: false, ease: "easeOutQuart"});


//       // Define Bottom Sheet animation
//       if ($modal.hasClass('bottom-sheet')) {
//         $modal.velocity({bottom: "-100%", opacity: 0}, {
//           duration: options.out_duration,
//           queue: false,
//           ease: "easeOutCubic",
//           // Handle modal ready callback
//           complete: function() {
//             $overlay.css({display:"none"});

//             // Call complete callback
//             if (typeof(options.complete) === "function") {
//               options.complete();
//             }
//             $overlay.remove();
//             _stack--;
//           }
//         });
//       }
//       else {
//         $modal.velocity(
//           { top: options.starting_top, opacity: 0, scaleX: 0.7}, {
//           duration: options.out_duration,
//           complete:
//             function() {

//               $(this).css('display', 'none');
//               // Call complete callback
//               if (typeof(options.complete) === "function") {
//                 options.complete();
//               }
//               $overlay.remove();
//               _stack--;
//             }
//           }
//         );
//       }
//     }
//   });

//   $.fn.extend({
//     leanModal: function(option) {
//       return this.each(function() {

//         var defaults = {
//           starting_top: '4%'
//         },
//         // Override defaults
//         options = $.extend(defaults, option);

//         // Close Handlers
//         $(this).click(function(e) {
//           options.starting_top = ($(this).offset().top - $(window).scrollTop()) /1.15;
//           var modal_id = $(this).attr("href") || '#' + $(this).data('target');
//           $(modal_id).openModal(options);
//           e.preventDefault();
//         }); // done set on click
//       }); // done return
//     }
//   });


//   };
