function init_picker(){
  filepicker.setKey('AwWNg6Ei3SHyfKegusrWIz');
  filepicker.pick(
    {
      extensions: ['.csv', 'xls', 'xlsx', '.gsheet', '.png'],
      services: ['COMPUTER', 'GOOGLE_DRIVE']
    },
    function(Blob){
      console.log(Blob.url);

      // On success update preview and send URL to flask to process
      // Update preview
      var fileId = Blob.url.substr(Blob.url.lastIndexOf('/') + 1);
      var previewUrl = "https://www.filestackapi.com/api/file/" + fileId;
      // var div = document.createElement("div");
      // //div.setAttribute("id", "file-preview");
      // div.setAttribute("type", "filepicker-preview")
      // div.setAttribute("data-fp-url", previewUrl);
      // div.setAttribute("style", "width:75%; height:1500px");
      //
      // $('body').append(div);

      //$('div[type=filepicker-preview]').setAttribute("data-fp-url", previewUrl);

      console.log("Redirecting")
      // Send URL to Flask
      var url = '/previewUpload';
      $.post(url,
        {
          url: Blob.url
        }
      )

    }
  );
}
