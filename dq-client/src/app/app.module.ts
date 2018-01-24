import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { routing } from './app.routes';

import { AppComponent } from './app.component';
import { TableListComponent } from './components/table-list/table-list.component';
import { DataService } from './services/data.service';
import { NewTableComponent } from './components/new-table/new-table.component';
import { TableDetailComponent } from './components/table-detail/table-detail.component';


@NgModule({
  declarations: [
    AppComponent,
    TableListComponent,
    NewTableComponent,
    TableDetailComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    routing
  ],
  providers: [
    {
      provide: 'data',
      useClass: DataService
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
