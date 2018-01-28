import { Component, OnInit, ViewChild, ElementRef, Inject} from '@angular/core';

import { Attribute } from '../../data-structure/attribute';
import { LOCALE_DATA } from '@angular/common/src/i18n/locale_data';

declare const Rickshaw: any;

declare const io: any;
// declare const Plotly: any;
@Component({
  selector: 'app-monitor',
  templateUrl: './monitor.component.html',
  styleUrls: ['./monitor.component.css']
})

export class MonitorComponent implements OnInit {

  // @ViewChild('chart') el: ElementRef;
  graph: any;
  constructor(@Inject('stream-data') private streamData) { }
  attribute: Attribute[];
  thisData: any;
  dataURL: any;
  socket: any;

  ngOnInit() {

    Rickshaw.Graph.Socketio.Static = Rickshaw.Class.create( Rickshaw.Graph.Socketio, {
      request: function() {
        var __this = this;
        this.socket = io();
        this.socket.on('rickshaw', function (data) {
          // console.log("Got some fancy Websocket data: ");
          // console.log(data);
          __this.success(data);
        });
      }
    } );

    var socketioGraph = new Rickshaw.Graph.Socketio.Static( {
      element: document.getElementById("chart"),
      width: 1000,
      height: 700,
      renderer: 'line',
      dataURL: "http://localhost",

      onData: function(d) { Rickshaw.Series.zeroFill(d); return d },
      
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
          // this.xAxis = new Rickshaw.Graph.Axis.Time({
          //   graph: transport.graph,
          //   timeUnit: seconds,
          //   timeFixture: new Rickshaw.Fixtures.Time.Local()
          // });

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
              return new Date(x * 1000).toString();
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
}
