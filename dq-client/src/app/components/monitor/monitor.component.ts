import { Component, OnInit, Inject} from '@angular/core';
import { NullAstVisitor } from '@angular/compiler';

declare const Rickshaw: any;
declare const io: any;

@Component({
  selector: 'app-monitor',
  templateUrl: './monitor.component.html',
  styleUrls: ['./monitor.component.css']
})



export class MonitorComponent implements OnInit {

  stream_attributes = ["rickshaw", "a", "b"]
  graph: any;
  constructor(@Inject('stream-data') private streamData) { }
  socket: any;
  selectedValue: string;
  socketioGraph: any;

  ngOnInit() {
    this.createGraph(this.stream_attributes[0]);

  }

  createGraph(attr: string) {

    Rickshaw.Graph.Socketio.Static = Rickshaw.Class.create( Rickshaw.Graph.Socketio, { 
      request: function() {
        const thisData = this;
        io().on('rickshaw', function (data) {
          console.log("Got some fancy Websocket data: ");
          console.log(data);
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
          
        var time = new Rickshaw.Fixtures.Time();
        var seconds = time.unit('second');    
        if (!this.yAxis) {
          this.yAxis = new Rickshaw.Graph.Axis.Y({
            graph: transport.graph,
            tickFormat: Rickshaw.Fixtures.Number.formatKMBT,            
          });
        }
        
        if (!this.xAxis) {

          var xAxis = new Rickshaw.Graph.Axis.Time( {
            graph: transport.graph,
            ticksTreatment: 'glow',
            timeFixture: new Rickshaw.Fixtures.Time.Local()
          } );         
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
  }


  onSelect(attr: string): void {
    this.selectedValue = attr;
    Rickshaw.Graph.Socketio.Static = Rickshaw.Class.create( Rickshaw.Graph.Socketio, { 
      request: function() {
        const thisData = this;
        io().on(this.selectedValue, function (data) {
          console.log("Got some fancy Websocket data: ");
          console.log(data);
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
      }
    });
  }

}
