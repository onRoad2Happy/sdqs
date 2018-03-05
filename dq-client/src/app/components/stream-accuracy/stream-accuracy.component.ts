import { Component, OnInit, Inject } from '@angular/core';
declare const io: any;

@Component({
  selector: 'app-stream-accuracy',
  templateUrl: './stream-accuracy.component.html',
  styleUrls: ['./stream-accuracy.component.css']
})
export class StreamAccuracyComponent implements OnInit {

  data = {};
  attributes = [];
  socket: any;

  constructor(@Inject('stream-data') private dataService) { }

  ngOnInit() {
    this.socket = io();
    this.getData();
  }


  getData = ()=> {    
        
    var data = this.data;
    var socket = this.socket;
    var select_attr = 'user_info_target';
    socket.emit('join', select_attr);    
    socket.on('create_room', function() {
      console.log(select_attr);
      socket.emit('getData', select_attr);
    })
    
    socket.on(select_attr, (r) => {
      console.log(r);
      this.data = r[0];
      this.attributes = Object.keys(r[0]);

    })
    

  }
  
}
