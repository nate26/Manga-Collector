import { Routes } from '@angular/router';
import { CollectionComponent } from './page-components/collection/collection.component';
import { SeriesViewComponent } from './views/series-view/series-view.component';
import { ListViewComponent } from './views/list-view/list-view.component';
import { GridViewComponent } from './views/grid-view/grid-view.component';

export const routes: Routes = [
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
