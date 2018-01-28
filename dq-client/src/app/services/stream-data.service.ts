import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Rx';

import 'rxjs/add/operator/toPromise';
import { Attribute } from '../data-structure/attribute';
declare const io: any;



@Injectable()
export class StreamDataService {
  private _attributeSource = new BehaviorSubject<Attribute[]>([]);
  // streamSocket = io();

  constructor(private http: Http) { }
  
}
