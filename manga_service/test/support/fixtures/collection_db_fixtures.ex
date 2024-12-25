defmodule MangaService.CollectionDBFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `MangaService.CollectionDB` context.
  """

  @doc """
  Generate a collection.
  """
  def collection_fixture(attrs \\ %{}) do
    {:ok, collection} =
      attrs
      |> Enum.into(%{
        collection: "some collection",
        cost: 120.5,
        id: "some id",
        isbn: "some isbn",
        purchase_date: ~D[2024-11-02],
        rating: 120.5,
        read: true,
        store: "some store",
        tags: ["option1", "option2"],
        user_id: "some user_id"
      })
      |> MangaService.CollectionDB.create_collection()

    collection
  end
end
