import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Rx';

import 'rxjs/add/operator/toPromise';

import { Table } from '../data-structure/table'
import { Attribute } from '../data-structure/attribute';

// const ATTRIBUTES: Attribute[] = [
//   {
//     name: "attr1",
//     count: 5,
//     max: 5,
//     min: 2,
//     mean: 3,
//     stddev: 2
//   },
//   {
//     name: "attr2",
//     count: 5,
//     max: 9,
//     min: 2,
//     mean: 3,
//     stddev: 2

//   }
// ];
// const TABLES: Table[] = [
//   {
//     id: 1,
//     name: "table1",
//     attributes: ATTRIBUTES
//   },
//   {
//     id: 2,
//     name: "table2",
//     attributes: ATTRIBUTES
//   }
// ]

@Injectable()
export class DataService {
  // tables: Table[] = TABLES;
  private _tableSource = new BehaviorSubject<Table[]>([]);


  constructor(private http: Http) { }

  getTables(): Observable<Table[]> {
    // return this.tables;
    this.http.get('api/v1/tables')
    .toPromise()
    .then((res: Response) => {
      this._tableSource.next(res.json());
    })
    .catch(this.handleError);
    return this._tableSource.asObservable();
  }

  getTable(id: number) {
    // return this.tables.find( table => table.id === id);
    return this.http.get(`api/v1/tables/${id}`).toPromise()
    .then((res: Response) => {
      return res.json();
    })
    .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.log('An error occur', error);
    return Promise.reject(error);
  }

}
