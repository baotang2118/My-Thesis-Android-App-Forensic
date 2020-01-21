import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {MafComponent} from './maf/maf.component';

const routes: Routes = [
  {
    path:  'maf-tool',
    component:  MafComponent,
  },
  { 
    path: '',
    redirectTo: '/maf-tool',
    pathMatch: 'full'
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
