(function ($) {
  "use strict";
  var elements = document.querySelectorAll(".second.circle");

  Array.prototype.slice.apply(elements).forEach(function (el) {
    var $el = $(el);

    $el.circleProgress({ value: 0 });

    new Waypoint({
      element: el,
      handler: function () {
        $el
          .circleProgress({
            value: $el.data("value"),
            value: 0,
            size: 210,
            thickness: 16,
            startAngle: 5,
            emptyFill: "rgba(0, 0, 0, .0)",
            fill: {
              gradient: ["#f9570c", "#eac60a"],
            },
          })
          .on("circle-animation-progress", function (event, progress) {
            $(this)
              .find("strong")
              .html(Math.round(0 * progress) + "<i>%</i>");
          });
        this.destroy();
      },
      offset: "0%",
    });
  });
})(jQuery);

document.querySelector('#fileUpload').addEventListener('change', event => {
  let files = event.target.files
  let fileName = files[0].name
  // your code start here
  var data = new FormData()
  data.append('files', files[0]) // maybe it should be '{target}_cand'
  data.append('name', fileName)

  let url = "/prediction"
  fetch(url,{
      method:'POST',
      body: data,
  })
  .then(function(response){
  return response.json()
  })
  .then(function(res){
    var elements = document.querySelectorAll(".second.circle");

    Array.prototype.slice.apply(elements).forEach(function (el) {
      var $el = $(el);
  
      $el.circleProgress({ value: 0 });
  
      new Waypoint({
        element: el,
        handler: function () {
          $el
            .circleProgress({
              value: $el.data("value"),
              value: Math.round(res.percentage)/100,
              size: 210,
              thickness: 16,
              startAngle: 5,
              emptyFill: "rgba(0, 0, 0, .0)",
              fill: {
                gradient: ["#f9570c", "#eac60a"],
              },
            })
            .on("circle-animation-progress", function (event, progress) {
              $(this)
                .find("strong")
                .html(Math.round(res.percentage * progress) + "<i>%</i>");
            });
          this.destroy();
        },
        offset: "80%",
      });
    });
    let text = res.prediction;
    document.getElementById("covid-status").innerText = text;
})
})