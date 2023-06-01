export default class Backend {
    async request(url, method='GET', data=undefined) {
        let headers;
        if (data !== undefined) {
            headers = { 'Content-Type': 'application/json' };
        }
    
        const requestOptions = {
            method: method,
            headers: headers,
            body: JSON.stringify(data)
        };
        
        const response = await fetch(url, requestOptions);
        return response.json();
    }

    async userStatus() {
        return this.request('/api/user/status').then((data) => data.login===true);
    }

    async userLogin(user, password) {
        return this.request('/api/user/login', 'POST',  { user, password }).then((data) => data.login===true);
    }

    async userRegister(user, password) {
        return this.request('/api/user/register', 'POST',  { user, password }).then((data) => data.login===true);
    }

    async userLogout() {
        return this.request('/api/user/logout', 'POST', {});
    }

    async resumeList() {
        return this.request('/api/resume/');
    }

    async resumeGet(id) {
        return this.request(`/api/resume/${id}/text`);
    }

    async resumeUpdate(id, text) {
        return this.request(`/api/resume/${id}/update`, 'POST', {text});
    }

    async resumeCreate(text) {
        return this.request(`/api/resume/create`, 'POST', {text});
    }

    async resumeDelete(id) {
        return this.request(`/api/resume/${id}/delete`, 'POST');
    }
}
