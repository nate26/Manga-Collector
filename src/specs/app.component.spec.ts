import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { AppComponent } from '../app/app.component';
import { HomeComponent } from '../app/home/home/home.component';
import { CollectionComponent } from '../app/page-components/collection/collection.component';

describe('AppComponent', () => {
  @Component({
    selector: 'app-home',
    imports: [],
    template: ``
  })
  class MockHomeComponent {}

  @Component({
    selector: 'app-collection',
    imports: [],
    template: ``
  })
  class MockCollectionComponent {}

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppComponent]
    })
      .overrideComponent(AppComponent, {
        remove: { imports: [HomeComponent, CollectionComponent] },
        add: { imports: [MockHomeComponent, MockCollectionComponent] }
      })
      .compileComponents();
  });
});
