function storeFile() {
  // Send URL to be processed in backend
  var url = '/storeFile';
  var file_url = window.event.fpfile["url"]
  $.post(url,
    {
      url: file_url
    },
    success = function(response) {
      if (response["success"]) {
        file_preview(file_url)
        Materialize.toast('File Upload Success', 4000, 'teal')
      }
      else {
        alert(response["error"]);
      }
    }
  )
}

function file_preview(file_url) {
  var fileId = file_url.substr(file_url.lastIndexOf('/') + 1);
  var previewUrl = "https://www.filestackapi.com/api/preview/" + fileId;
  var div = document.createElement("div");
  $('iframe[src*="https://www.filestackapi.com/api/preview/"]')[0].setAttribute("src", previewUrl)
}
