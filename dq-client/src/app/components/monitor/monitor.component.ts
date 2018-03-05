import { Component, OnInit, Inject} from '@angular/core';
import { NullAstVisitor } from '@angular/compiler';

declare const Rickshaw: any;
declare const io: any;
declare const moment: any;
@Component({
  selector: 'app-monitor',
  templateUrl: './monitor.component.html',
  styleUrls: ['./monitor.component.css']
})



export class MonitorComponent implements OnInit {

  stream_attributes = ["a", "b", "c"]
  graph: any;
  constructor(@Inject('stream-data') private streamData) { }
  selectedValue = this.stream_attributes[0];
  socketioGraph: any;
  socket: any;
  ngOnInit() {    
    this.createGraph();  
  }

  createGraph() {    
    this.socket = io();

    var socket = this.socket;
    var select_attr = this.selectedValue;
    socket.emit('joinMonitor', select_attr);
    
    socket.on('create_room', function(){
      socket.emit('getGraphData', select_attr);
    })

    var attr = this.selectedValue;

    Rickshaw.Graph.Socketio.Static = Rickshaw.Class.create( Rickshaw.Graph.Socketio, { 
      request: function() {
        const thisData = this;    
        socket.on(attr, function (data) {
          thisData.success(data);
        });        
      }
    } );
    this.socketioGraph = new Rickshaw.Graph.Socketio.Static( {
      element: document.getElementById("chart"),
      width: 600,
      height: 400,
      renderer: 'line',
      // dataURL: "http://localhost",
       
    

      onData: function(d) {
        Rickshaw.Series.zeroFill(d); 
        return d;
      },

      onComplete: function(transport) {        
        var tv = 250;

        var time = new Rickshaw.Fixtures.Time();
        var seconds = time.unit('second');    
        if (!this.yAxis) {
          this.yAxis = new Rickshaw.Graph.Axis.Y({
            graph: transport.graph,
            tickFormat: Rickshaw.Fixtures.Number.formatKMBT,            
          });
        }
        
        if (!this.xAxis) {

          var unit = {}

          unit['formatTime'] = function(d) {      
            return moment(d).format("HH:mm:ss");      
          };
          unit['formatter'] = function(d) { return this.formatTime(d)};
          unit['name'] = "15 second";
          unit['seconds'] = 15;
          var xAxis = new Rickshaw.Graph.Axis.Time({
            graph: transport.graph,
            timeUnit:unit,
            ticksTreatment: 'glow',
            timeFixture: new Rickshaw.Fixtures.Time.Local()
          });
          
      
        }
        

        if (!this.hoverDetail) {
          this.hoverDetail = new Rickshaw.Graph.HoverDetail( {
            graph: transport.graph,
            xFormatter: function(x) {
              return new Date(x*1000).toString();
            }          
          } );
  
        }
        if (!this.legend) {
          this.legend = new Rickshaw.Graph.Legend( {
            graph: transport.graph,
            element: document.getElementById('legend')
          } );
        }
        
        if (!this.shelving) {
          this.shelving = new Rickshaw.Graph.Behavior.Series.Toggle( {
           graph: transport.graph,
          legend: this.legend
        } );
        }
        
        if (!this.order) {
        this.order = new Rickshaw.Graph.Behavior.Series.Order( {
          graph: transport.graph,
          legend: this.legend
        } );
  
        }
        if (!this.highlight) {
          this.highlight = new Rickshaw.Graph.Behavior.Series.Highlight( {
          graph: transport.graph,
          legend: this.legend
        } );
        }        
      
      } 

    } );


    
        
    socket.on('disconnect', function(){
      console.log('browser close');
      var attr = this.selectedValue;      
      // socket.disconnect();
    })

    
  }


  onSelect(attr: string): void {    
    // this mean new clinet
    this.clearGraph();
    this.socket.disconnect();
    this.selectedValue = attr;    
    this.createGraph();    
  }

  clearGraph() {
    document.getElementById('legend').remove();
    document.getElementById('chart').remove();
    document.getElementById("chart_container").insertAdjacentHTML('beforeend', '<div id="chart"></div><div id="legend_container"><div id="smoother" title="Smoothing"></div><div id="legend"></div></div>  <div id="slider"></div>')
  }

}
