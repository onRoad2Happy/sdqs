import { Component, OnInit, Inject} from '@angular/core';
import { ActivatedRoute, Params} from '@angular/router';
import { Table } from '../../data-structure/table';

@Component({
  selector: 'app-table-detail',
  templateUrl: './table-detail.component.html',
  styleUrls: ['./table-detail.component.css']
})
export class TableDetailComponent implements OnInit {
  table: Table;
  selectedValue: string;
  view = [];
  attrs = [];

  constructor(
    private route: ActivatedRoute,
    @Inject('data') private data
  ) { }

  ngOnInit() {
    this.route.params.subscribe((params: Params) => {      
      // this.table = this.data.getTable(+params['id']);
      this.data.getTable(+params['id'])
      .then(table => {
        this.table = table;
        this.view = table['summary'];
        if (this.view && this.view.length !== 0) {
          this.attrs = Object.keys(this.view[0]);
        }      
      });
    });


  } 

  formatNumber(i) {
    return Math.round(i * 100)/100; 
  }

}
