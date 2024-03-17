class Api {
  constructor(url, headers) {
    this._url = url;
    this._headers = headers;
  }

  checkResponse(res) {
    return new Promise((resolve, reject) => {
      if (res.status === 204) {
        return resolve(res);
      }
      const func = res.status < 400 ? resolve : reject;
      res.json().then((data) => func(data));
    });
  }

  checkFileDownloadResponse(res) {
    return new Promise((resolve, reject) => {
      if (res.status < 400) {
        return res.blob().then((blob) => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "shopping-list";
          document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
          a.click();
          a.remove(); //afterwards we remove the element again
        });
      }
      reject();
    });
  }

  signin({ email, password }) {
    return fetch("/api/v1/auth/token/login/", {
      method: "POST",
      headers: this._headers,
      body: JSON.stringify({
        email,
        password,
      }),
    }).then(this.checkResponse);
  }

  signout() {
    const token = localStorage.getItem("token");
    return fetch("/api/v1/auth/token/logout/", {
      method: "POST",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  signup({ email, password, username, first_name, last_name }) {
    return fetch(`/api/v1/users/`, {
      method: "POST",
      headers: this._headers,
      body: JSON.stringify({
        email,
        password,
        username,
        first_name,
        last_name,
      }),
    }).then(this.checkResponse);
  }

  getUserData() {
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/users/me/`, {
      method: "GET",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  changePassword({ current_password, new_password }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/users/set_password/`, {
      method: "POST",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
      body: JSON.stringify({ current_password, new_password }),
    }).then(this.checkResponse);
  }

  // recipes

  getRecipes({
    page = 1,
    limit = 6,
    is_teacher = 0,
    is_staff,
    is_in_students = 0,
    teacher,
    rubric,
    my,
  } = {}) {
    const token = localStorage.getItem("token");
    const authorization = token ? { authorization: `Token ${token}` } : {};
    const rubricsString = rubric
      ? rubric
          .filter((rubric) => rubric.value)
          .map((rubric) => `&rubric=${rubric.slug}`)
          .join("")
      : "";
    return fetch(
      `/api/v1/groups/?page=${page}&limit=${limit}${
        teacher ? `&teacher=${teacher}` : ""
      }${rubricsString}${
        is_in_students ? `&is_in_students=${is_in_students}` : ""
      }${my ? `&my=${my}` : ""}`,
      {
        method: "GET",
        headers: {
          ...this._headers,
          ...authorization,
        },
      }
    ).then(this.checkResponse);
  }

  getRecipe({ recipe_id }) {
    const token = localStorage.getItem("token");
    const authorization = token ? { authorization: `Token ${token}` } : {};
    return fetch(`/api/v1/groups/${recipe_id}/`, {
      method: "GET",
      headers: {
        ...this._headers,
        ...authorization,
      },
    }).then(this.checkResponse);
  }

  createRecipe({
    name = "",
    title = "",
    image,
    rubric = [],
    number_of_lessons = 0,
    description = "",
    begin_at,
    //ingredients = []
  }) {
    const token = localStorage.getItem("token");
    return fetch("/api/v1/groups/", {
      method: "POST",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
      body: JSON.stringify({
        name,
        title,
        image,
        rubric,
        number_of_lessons,
        description,
        begin_at,
      }),
    }).then(this.checkResponse);
  }

  updateRecipe(
    {
      name,
      recipe_id,
      title,
      image,
      rubric,
      number_of_lessons,
      description,
      begin_at,
    },
    wasImageUpdated
  ) {
    // image was changed
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/groups/${recipe_id}/`, {
      method: "PATCH",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
      body: JSON.stringify({
        name,
        id: recipe_id,
        title,
        image: wasImageUpdated ? image : undefined,
        rubric,
        number_of_lessons: Number(number_of_lessons),
        description,
        begin_at,
      }),
    }).then(this.checkResponse);
  }

  addToJoinings({ id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/groups/${id}/join/`, {
      method: "POST",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  removeFromJoinings({ id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/groups/${id}/join/`, {
      method: "DELETE",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  getUser({ id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/users/${id}/`, {
      method: "GET",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  getUsers({ page = 1, limit = 6 }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/users/?page=${page}&limit=${limit}`, {
      method: "GET",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  // subscriptions

  getSubscriptions({ page, limit = 6, recipes_limit = 3 }) {
    const token = localStorage.getItem("token");
    return fetch(
      `/api/users/subscriptions/?page=${page}&limit=${limit}&recipes_limit=${recipes_limit}`,
      {
        method: "GET",
        headers: {
          ...this._headers,
          authorization: `Token ${token}`,
        },
      }
    ).then(this.checkResponse);
  }

  deleteSubscriptions({ author_id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/users/${author_id}/subscribe/`, {
      method: "DELETE",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  subscribe({ author_id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/users/${author_id}/subscribe/`, {
      method: "POST",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  // ingredients
  getSchedule({ group_id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/groups/${group_id}/schedule_items/`, {
      method: "GET",
      headers: {
        ...this._headers,
      },
    }).then(this.checkResponse);
  }

  createSchedule({ group_id, day_of_week = 0, btime }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/groups/${group_id}/schedule_items/`, {
      method: "POST",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
      body: JSON.stringify({
        day_of_week,
        btime,
      }),
    }).then(this.checkResponse);
  }

  deleteSchedule({ group_id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/groups/${group_id}/schedule_items/`, {
      method: "DELETE",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  getRings() {
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/rings`, {
      method: "GET",
      headers: {
        ...this._headers,
      },
    }).then(this.checkResponse);
  }

  // tags
  getTags() {
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/rubrics/`, {
      method: "GET",
      headers: {
        ...this._headers,
      },
    }).then(this.checkResponse);
  }

  addToOrders({ id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/recipes/${id}/shopping_cart/`, {
      method: "POST",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  removeFromOrders({ id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/recipes/${id}/shopping_cart/`, {
      method: "DELETE",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  deleteRecipe({ recipe_id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/groups/${recipe_id}/`, {
      method: "DELETE",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  downloadFile() {
    const token = localStorage.getItem("token");
    return fetch(`/api/recipes/download_shopping_cart/`, {
      method: "GET",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkFileDownloadResponse);
  }

  createLessons({ group_id }) {
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/groups/${group_id}/forming`, {
      method: "POST",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }

  getLessons() {
    const token = localStorage.getItem("token");
    return fetch(`/api/v1/lessons`, {
      method: "GET",
      headers: {
        ...this._headers,
        authorization: `Token ${token}`,
      },
    }).then(this.checkResponse);
  }
}
export default new Api(process.env.API_URL || "http://localhost", {
  "content-type": "application/json",
});
