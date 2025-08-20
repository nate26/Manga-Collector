defmodule MangaService.UserDBFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `MangaService.UserDB` context.
  """

  @doc """
  Generate a user.
  """
  def user_fixture(attrs \\ %{}) do
    {:ok, user} =
      attrs
      |> Enum.into(%{
        banner: "some banner",
        collection_id: "some collection_id",
        color: "some color",
        email: "some email",
        id: "some id",
        password: "some password",
        personal_stores: ["option1", "option2"],
        picture: "some picture",
        theme: "some theme",
        username: "some username"
      })
      |> MangaService.UserDB.create_user()

    user
  end
end
