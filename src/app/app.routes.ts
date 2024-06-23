import { Routes } from '@angular/router';
import { CollectionComponent } from './page-components/collection/collection.component';
import { SeriesComponent } from './page-components/series/series.component';
import { LoginComponent } from './home/login/login.component';
import { loggedInGuard } from './guards/logged-in.guard';
import { PageNotFoundComponent } from './home/page-not-found/page-not-found.component';

export const routes: Routes = [
    {
        path: '',
        redirectTo: '/login',
        pathMatch: 'full'
    },
    {
        path: 'login',
        component: LoginComponent,
        canActivate: [loggedInGuard]
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
