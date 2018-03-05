import { Component, OnInit, Inject } from '@angular/core';
declare const io: any;

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  public table = [];
  public data = [];
  socket: any;

  constructor(@Inject('stream-data') private dataService) { }

  ngOnInit() {
    this.socket = io();
    this.getData();
  }


  getData = ()=> {    
        
    var data = this.data;
    var socket = this.socket;
    var select_attr = 'stream';
    socket.emit('join', select_attr);
    
    socket.on('create_room', function() {
      console.log(select_attr);
      socket.emit('getData', select_attr);
    })
    socket.on(select_attr, (r) => {
      this.data = r;
      if (this.data.length !== 0) {
        this.table = Object.keys(r[0]);
      }
    })
    

  }

}
