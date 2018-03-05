import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Rx';

import 'rxjs/add/operator/toPromise';
import { Attribute } from '../data-structure/attribute';
import { of } from 'rxjs/observable/of';

declare const io: any;

@Injectable()
export class StreamDataService {

  private _dataSource = new BehaviorSubject<{}>({});

  socket: any;

  constructor() { }
  
}



