defmodule MangaService.FollowedDBFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `MangaService.FollowedDB` context.
  """

  @doc """
  Generate a followed.
  """
  def followed_fixture(attrs \\ %{}) do
    {:ok, followed} =
      attrs
      |> Enum.into(%{
        follow_id: "some follow_id",
        follow_type: "some follow_type",
        user_id: "some user_id"
      })
      |> MangaService.FollowedDB.create_followed()

    followed
  end
end
