import { TestBed } from '@angular/core/testing';
import { AppComponent } from '../app/app.component';
import { Component } from '@angular/core';
import { HomeComponent } from '../app/home/home/home.component';
import { CollectionComponent } from '../app/page-components/collection/collection.component';

describe('AppComponent', () => {

    @Component({
        selector: 'app-home',
        standalone: true,
        imports: [],
        template: ``
    })
    class MockHomeComponent { }

    @Component({
        selector: 'app-collection',
        standalone: true,
        imports: [],
        template: ``
    })
    class MockCollectionComponent { }

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [AppComponent]
        }).overrideComponent(AppComponent, {
            remove: { imports: [HomeComponent, CollectionComponent] },
            add: { imports: [MockHomeComponent, MockCollectionComponent] }
        }).compileComponents();
    });

    it('should create the app', () => {
        const fixture = TestBed.createComponent(AppComponent);
        const app = fixture.componentInstance;
        expect(app).toBeTruthy();
    });

});
