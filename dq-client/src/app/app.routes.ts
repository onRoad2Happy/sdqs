import { Routes, RouterModule } from '@angular/router';
import { TableListComponent } from './components/table-list/table-list.component';
import { TableDetailComponent } from './components/table-detail/table-detail.component';


const routes: Routes = [
  {
      path: '',
      redirectTo: 'tables',
      pathMatch: 'full'
  },
  {
      path: 'tables',
      component: TableListComponent
  },
  {
      path: 'tables/:id',
      component: TableDetailComponent
  },
  {
      path: '**',
      redirectTo: 'tables'
  }


];

export const routing = RouterModule.forRoot(routes);