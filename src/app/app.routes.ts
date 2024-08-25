import { Routes } from '@angular/router';
import { CollectionComponent } from './page-components/collection/collection.component';
import { SeriesComponent } from './page-components/series/series.component';
import { loggedInGuard } from './guards/logged-in.guard';
import { PageNotFoundComponent } from './home/page-not-found/page-not-found.component';

export const routes: Routes = [
    {
        path: '',
        redirectTo: '/collection',
        pathMatch: 'full'
    },
    {
        path: 'collection',
        component: CollectionComponent,
        canActivate: [loggedInGuard]
    },
    {
        path: 'series',
        component: SeriesComponent,
        canActivate: [loggedInGuard]
    },
    {
        path: '**',
        component: PageNotFoundComponent
    }
];
