import { Component, OnInit, Inject } from '@angular/core';
import { Table } from '../../data-structure/table'

@Component({
  selector: 'app-table-list',
  templateUrl: './table-list.component.html',
  styleUrls: ['./table-list.component.css']
})
export class TableListComponent implements OnInit {
  tables: Table[] = [];
  constructor(@Inject('data') private dataService) { }

  ngOnInit() {
    this.getTables();
  }

  getTables(): void {
    // this.tables = this.dataService.getTables();
    this.dataService.getTables()
    .subscribe(tables => this.tables = tables);
    
  }

}
