import { Routes } from '@angular/router';
import { CollectionComponent } from './page-components/collection/collection.component';
import { SeriesComponent } from './page-components/series/series.component';
import { loggedInGuard } from './guards/logged-in.guard';
import { PageNotFoundComponent } from './home/page-not-found/page-not-found.component';
import { BrowseSalesComponent } from './page-components/browse-sales/browse-sales.component';
import { SeriesDetailsComponent } from './page-components/series-details/series-details.component';

export const routes: Routes = [
    {
        path: '',
        redirectTo: '/sales',
        pathMatch: 'full'
    },
    {
        path: 'sales',
        component: BrowseSalesComponent
    },
    {
        path: 'series',
        component: SeriesComponent,
        canActivate: [loggedInGuard]
    },
    {
        path: 'series/:series_id',
        component: SeriesDetailsComponent,
        canActivate: [loggedInGuard]
    },
    {
        path: 'collection',
        component: CollectionComponent,
        canActivate: [loggedInGuard]
    },
    {
        path: '**',
        component: PageNotFoundComponent
    }
];
