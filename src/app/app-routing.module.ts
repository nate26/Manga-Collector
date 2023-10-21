import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CollectionComponent } from './page-components/collection/collection.component';
import { SeriesViewComponent } from './views/series-view/series-view.component';
import { ListViewComponent } from './views/list-view/list-view.component';
import { GridViewComponent } from './views/grid-view/grid-view.component';

const routes: Routes = [
    {
        path: 'collection',
        component: CollectionComponent,
        children: [
            {
                path: 'grid',
                component: GridViewComponent
            },
            {
                path: 'list',
                component: ListViewComponent
            },
            {
                path: 'series',
                component: SeriesViewComponent
            }
        ]
    },
    {
        path: '',
        redirectTo: 'collection',
        pathMatch: 'full'
    }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
