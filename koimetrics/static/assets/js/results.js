// MAP DATA

  var heat;
  var mymap;
  var locations;
  var group;
  var LeafIcon = L.Icon.extend({
    options: {
      iconSize: [20, 30],
      shadowAnchor: [8, 20],
      shadowSize: [0, 0],
      iconSize: [20, 25],
      iconAnchor: [8, 30] // horizontal puis vertical
    }
  });
  var redIcon = new LeafIcon({ iconUrl: "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2Fe%2Fed%2FMap_pin_icon.svg%2F1200px-Map_pin_icon.svg.png&f=1&nofb=1" });

  setTimeout(function () {
    mymap = L.map('mapid').setView([28.505, -0.09], 1);;
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
      maxZoom: 10,
      minZoom: 1,
      attribution: '',
      id: 'mapbox/streets-v11',
      tileSize: 512,
      zoomOffset: -1,
    }).addTo(mymap);
    group = L.layerGroup([]);
    if (connected_users.length) {
      locations = connected_users.map((el) => [el.latitude, el.longitude]);
      group = L.layerGroup(connected_users.map((el) => L.marker([el.latitude, el.longitude], { icon: redIcon }).bindPopup(el.ip)));
      //mymap.fitBounds(group.getBounds());
      //heat = L.heatLayer(locations, { radius: 25 });
    }
    mymap.addLayer(group);
    mymap.setMaxBounds(mymap.getBounds());
  }, 1000);

  setInterval(function () {
    mymap.removeLayer(group);
    locations = connected_users.map((el) => [el.latitude, el.longitude]);
    group = new L.featureGroup(connected_users.map((el) => L.marker([el.latitude + Math.random() * 0.001, el.longitude + Math.random() * 0.001], { icon: redIcon }).bindPopup(el.ip)));
    //heat = L.heatLayer(locations, { radius: 25 });
    mymap.addLayer(group);
    if (locations.length) {
    }
  }, 1000);

// Realtime connected users

function getData() {
  return connected_users.length
}

var layout = {
  title: 'Online users',
  title: true,
  margin: {
    l: 80,
    r: 30,
    b: 50,
    t: 30,
    pad: 5
  },
  autosize: true,
  height: 400,

  xaxis: {
    title: {
      text: 'Seconds',
      font: {
        family: 'Courier New, monospace',
        size: 18,
        color: '#7f7f7f'
      }
    },
  },
  yaxis: {
    title: {
      text: 'Online visitors',
      font: {
        family: 'Courier New, monospace',
        size: 18,
        color: '#7f7f7f'
      }
    }
  }
};

setTimeout(function () {
  Plotly.plot('rt_chart', [{
    y: [getData()],
    type: 'line',
  }], layout, { displayModeBar: false })
  var cnt = 0;
  setInterval(function () {
    Plotly.extendTraces('rt_chart', { y: [[getData()]] }, [0])
    cnt++;
    if (cnt > 60) {
      Plotly.relayout('rt_chart', {
        xaxis: {
          range: [cnt - 60, cnt]
        }
      })
    }
  }, 1000)
}, 1500)



// Realtime  bar chart
var barchart;
  setTimeout(function () {
    barchart = new CanvasJS.Chart("barChartContainer", {
      title:{
        text: ""              
      },
      axisY: {
        title: "Online visitors",
      },
      axisX: {
        title: "website pages",
      },
      data: [              
      {
        // Change type to "doughnut", "line", "splineArea", etc.
        type: "column",
        dataPoints: [
          
        ]
      }
      ]
    });
    barchart.render();
  }, 1500);

  function updatePagesViewsChart() {
    var pages_list = [];
    Object.keys(pages).forEach( (k) => pages_list.push({page: k, views: pages[k]}) )
    pages_list.sort( (a,b) => (a.views > b.views) ? 1 : -1 );
    var dps = [];
    pages_list.forEach(function(p){
      dps.push( {label: website + p.page, x: dps.length, y: p.views} );
    });

    barchart.options.data[0].dataPoints = dps; 
    barchart.render();
  };
  setInterval(function() {updatePagesViewsChart()}, 2500);
  
// Realtime sessions table
var table_sessions = {};
var table_sessions_list = [];
function findObjectInArrayByProperty(array, propertyName, propertyValue) {
  return array.find((o) => { return o[propertyName] === propertyValue });
}

var clusterize_data = ['<td>Loading data</td>'];
var clusterize = new Clusterize({
  rows: clusterize_data,
  scrollId: 'scrollArea',
  contentId: 'contentArea', 
});

function updateTableSessions(){
    clusterize_data = ['<td>No data</td>'];
    if (connected_users.length){
      clusterize_data = [
        `<tr>
         <th scope="col">IP</th>
         <th scope="col">Location</th>
         <th scope="col">Page</th>
         <th scope="col">Device</th>
         </tr>`
      ];
    }
    var filter_rows = $(".sessions-filter").val().toLowerCase().replace(" ", "");
    var row = "";
    var str_ftr = "";
    connected_users.forEach((session)=>{
        row = `
          <tr >
            <td>${session.ip}</td>
            <td><img style='height: 22px' src='https://www.countryflags.io/${session.countrycode}/flat/64.png'> ${session.country},  ${session.city}</td>
            <td> ${session.path}</td>
            <td>${session.browser},  ${session.os}</td>
          </tr>
          `;
        if (filter_rows){
          
          if ( 
              session.ip.toLowerCase().includes(filter_rows) || 
              (session.country.toLowerCase()+","+session.city.toLowerCase()).includes(filter_rows) ||
              session.country.toLowerCase().includes(filter_rows) ||
              session.city.toLowerCase().includes(filter_rows) || 
              session.path.toLowerCase().includes(filter_rows) || 
              (session.browser.toLowerCase()+","+session.os.toLowerCase()).includes(filter_rows)  || 
              session.browser.toLowerCase().includes(filter_rows) || session.os.toLowerCase().includes(filter_rows) 
            )
            {
            clusterize_data.push(row);
          }
        } else {
          clusterize_data.push( row );
        }
  });
  clusterize.update(clusterize_data);
}

setInterval(updateTableSessions, 2500);

