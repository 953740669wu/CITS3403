// Get element
var box = document.getElementById("box");
var screen = box.children[0];
var ul = screen.children[0];
var ol = screen.children[1];
var lisUl = ul.children;

// Get picture width
var imgWid = screen.offsetWidth;

// Get left and right buttons
var arr = box.children[1];
var arrLeft = arr.children[0];
var arrRight = arr.children[1];

// Get the li creation in set ol based on getting the number of elements in lisUl
for (var i = 0; i < lisUl.length; i++) {
    var li = document.createElement("li");
    // put it in ol
    ol.appendChild(li);
    // set the content of li
    li.innerHTML = i + 1;
}

// Set the button click effect
// Set the first ul element
var lisOl = ol.children;
lisOl[0].className = "current";

for (var i = 0; i < lisOl.length; i++) {
    lisOl[i].index = i;
    lisOl[i].onclick = function () {
        for (var j = 0; j < lisOl.length; j++) {
            lisOl[j].className = "";
        }
        this.className = "current";
        animate(ul, -this.index * imgWid);
        pic = this.index; // update pic index
    };
}

// Clone the first picture and append it to ul
var firstPic = lisUl[0].cloneNode(true);
ul.appendChild(firstPic);

// Set ul width dynamically
ul.style.width = imgWid * (lisUl.length + 1) + "px";

// Click the right button
var pic = 0;
arrRight.onclick = function () {
    if (pic == lisUl.length - 1) {
        ul.style.left = 0 + "px";
        pic = 0;
    }
    pic++;
    // Let ul roll according to pic value
    animate(ul, -pic * imgWid);

    for (var i = 0; i < lisOl.length; i++) {
        lisOl[i].className = "";
    }

    if (pic == lisUl.length - 1) {
        lisOl[0].className = "current";
    } else {
        lisOl[pic].className = "current";
    }
};

// Click the left button
arrLeft.onclick = function () {
    if (pic == 0) {
        ul.style.left = -(ul.offsetWidth - imgWid) + "px";
        pic = lisUl.length - 1;
    }
    pic--;
    // Let ul roll according to pic value
    animate(ul, -pic * imgWid);

    for (var i = 0; i < lisOl.length; i++) {
        lisOl[i].className = "";
    }
    lisOl[pic].className = "current";
};

// Auto rolling
var timer = null;

function startAutoPlay() {
    if (timer === null) {
        timer = setInterval(function () {
            // Trigger the right button click event
            arrRight.click();
        }, 4000);
    }
}

function stopAutoPlay() {
    clearInterval(timer);
    timer = null;
}

startAutoPlay();

box.onmouseover = function () {
    arr.style.display = "block";
    stopAutoPlay();
};

box.onmouseout = function () {
    arr.style.display = "none";
    startAutoPlay();
};

function animate(tag, target) {
    clearInterval(tag.timer);
    tag.timer = setInterval(function () {
        var leader = tag.offsetLeft;
        var step = (target - leader) / 10; // Calculate step size dynamically
        step = step > 0 ? Math.ceil(step) : Math.floor(step);
        leader = leader + step;
        tag.style.left = leader + "px";

        if (leader === target) {
            clearInterval(tag.timer);
        }
    }, 30);
}
