var video = document.querySelector('video')
  , container = document.querySelector('#container');

var setVideoDimensions = function () {
  // Video's intrinsic dimensions
  var w = video.videoWidth
    , h = video.videoHeight;

  // Intrinsic Ratio
  // Will be more than 1 if W > H and less if W < H
  var videoRatio = (w / h).toFixed(2);

  // Get the container's computed styles
  //
  // Also calculate the min dimensions required (this will be
  // the container dimentions)
  var containerStyles = window.getComputedStyle(container)
    , minW = parseInt( containerStyles.getPropertyValue('width') )
    , minH = parseInt( containerStyles.getPropertyValue('height') );

  // What's the min:intrinsic dimensions
  //
  // The idea is to get which of the container dimension
  // has a higher value when compared with the equivalents
  // of the video. Imagine a 1200x700 container and
  // 1000x500 video. Then in order to find the right balance
  // and do minimum scaling, we have to find the dimension
  // with higher ratio.
  //
  // Ex: 1200/1000 = 1.2 and 700/500 = 1.4 - So it is best to
  // scale 500 to 700 and then calculate what should be the
  // right width. If we scale 1000 to 1200 then the height
  // will become 600 proportionately.
  var widthRatio = minW / w
    , heightRatio = minH / h;

  // Whichever ratio is more, the scaling
  // has to be done over that dimension
  if (widthRatio > heightRatio) {
    var newWidth = minW;
    var newHeight = Math.ceil( newWidth / videoRatio );
  }
  else {
    var newHeight = minH;
    var newWidth = Math.ceil( newHeight * videoRatio );
  }

  video.style.width = newWidth + 'px';
  video.style.height = newHeight + 'px';
};

video.addEventListener('loadedmetadata', setVideoDimensions, false);
window.addEventListener('resize', setVideoDimensions, false);



// Service Estimate Form Validation
function validateform()
{
  var passingFlag = true;
  var form = document.forms['estimateform'];

  name = form.name.value;
  email = form.email.value;
  phone = form.phone.value;
  subject = form.subject.value;
  message = form.message.value;

  if (name == "")
  {
    alert("Please enter a valid name")
    passingFlag = false;
  } else if (email == "" || !email.includes('@'))
  {
    alert("Please enter a valid email")
    passingFlag = false;
  } else if (phone == "" || !phone.match(/^\d+$/))
  {
    alert("Please enter a valid phone number with only numerical digits. \n Ex: 48022228888")
    passingFlag = false;
  } else if (subject == "")
  {
    alert("Please enter a subject")
    passingFlag = false;
  } else if (message = "")
  {
    alert("Please enter a message")
    passingFlag = false;
  }
  return passingFlag;
}

// Submit function
function submitform()
{
  if(validateform() === true)
  {
     setTimeout('window.location.href=submitted', 0);
  }
  if(validateform() === false)
  {
    setTimeout('window.location.href=contact', 0);
  }
}
