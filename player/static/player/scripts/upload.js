var tilesContainer = document.getElementById('tiles-container');
var fileInputContainer = document.getElementById('file-input-container');
var inputId = 0;

function addTile(index, inputId) {
  var tile = document.createElement('li');
  tile.className = 'mdc-grid-tile';
  tile.dataset.inputId = inputId;
  tile.dataset.index = index;
  tile.innerHTML = `
    <div class="mdc-grid-tile__primary">
      <img class="mdc-grid-tile__primary-content" src="">
    </div>
    <span class="mdc-grid-tile__secondary">
      <!--<i class="mdc-grid-tile__icon material-icons"
          onclick="deleteTile(this.parentNode.parentNode)">
        delete
      </i>-->
      <span class="mdc-grid-tile__title"></span>
      <span class="mdc-grid-tile__support-text"></span>
    </span>
  `;
  tilesContainer.appendChild(tile);
  
  return tile;
}

function titleCase(string) {
  return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}

var imageNameRegex = /3DIMG_(\d{2})(\w{3})(\d{4})_(\d{2})(\d{2})_.+\.jpg/i

function addFileInput() {
  inputId++;
  var fileInput = document.createElement('input');
  fileInput.id = 'file-input-' + inputId;
  fileInput.name = 'file-input-' + inputId;
  fileInput.type = 'file';
  fileInput.multiple = true;
  
  fileInput.addEventListener('change', function() {
    var images = this.files;
    for (var i = 0; i < images.length; i++) {
      var imagePath = window.URL.createObjectURL(images[i]);
      var imageName = images[i].name;
      
      var matches = imageNameRegex.exec(imageName);
      if (matches) {
        tile = addTile(i, fileInput.id);

        var day = matches[1];
        var month = titleCase(matches[2]);
        var year = matches[3];
        var hour = matches[4];
        var minute = matches[5];
        
        for (var c = 0; c < tile.children.length; c++) {
          var child = tile.children[c];
          for (var e = 0; e < child.children.length; e++) {
            var element = child.children[e];
            if (element.className == 'mdc-grid-tile__primary-content') {
              element.src = imagePath;
            }
            else if (element.className == 'mdc-grid-tile__title') {
              element.innerHTML = day + " " + month + " " + year;
            }
            else if (element.className == 'mdc-grid-tile__support-text') {
              element.innerHTML = hour + ":" + minute;
            }
          }
        }
      }
    }
  });
  
  fileInputContainer.appendChild(fileInput);
  
  $(fileInput).trigger('click');
}

function deleteTile(tile) {
  tile.parentNode.removeChild(tile);
};
