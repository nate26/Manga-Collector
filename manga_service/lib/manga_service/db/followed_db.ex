defmodule MangaService.FollowedDB do
  @moduledoc """
  The FollowedDB context.
  """

  import Ecto.Query, warn: false
  alias MangaService.Repo

  alias MangaService.FollowedDB.Followed

  @doc """
  Returns the list of followed.

  ## Examples

      iex> list_followed()
      [%Followed{}, ...]

  """
  def list_followed do
    Repo.all(Followed)
  end

  @doc """
  Gets a single followed.

  Raises `Ecto.NoResultsError` if the Followed does not exist.

  ## Examples

      iex> get_followed!(123)
      %Followed{}

      iex> get_followed!(456)
      ** (Ecto.NoResultsError)

  """
  def get_followed(id), do: Repo.get(Followed, id)

  @doc """
  Creates a followed.

  ## Examples

      iex> create_followed(%{field: value})
      {:ok, %Followed{}}

      iex> create_followed(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_followed(attrs \\ %{}) do
    %Followed{}
    |> Followed.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a followed.

  ## Examples

      iex> update_followed(followed, %{field: new_value})
      {:ok, %Followed{}}

      iex> update_followed(followed, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_followed(%Followed{} = followed, attrs) do
    followed
    |> Followed.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a followed.

  ## Examples

      iex> delete_followed(followed)
      {:ok, %Followed{}}

      iex> delete_followed(followed)
      {:error, %Ecto.Changeset{}}

  """
  def delete_followed(%Followed{} = followed) do
    Repo.delete(followed)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking followed changes.

  ## Examples

      iex> change_followed(followed)
      %Ecto.Changeset{data: %Followed{}}

  """
  def change_followed(%Followed{} = followed, attrs \\ %{}) do
    Followed.changeset(followed, attrs)
  end
end
