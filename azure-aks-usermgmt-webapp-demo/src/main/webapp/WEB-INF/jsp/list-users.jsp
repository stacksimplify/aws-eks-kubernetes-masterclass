<%@ include file="common/header.jspf" %>
<%@ include file="common/navigation.jspf" %>
	  <h2 class="text-center">List Users</h2>
 
	<div class="container">
		<div>
			<a type="button" class="btn btn-primary pull-right" href="/add-user">Create User</a>
		</div>	 
		<table class="table table-hover">
			<thead>
				<tr>
					<th>userid</th>
					<th>username</th>
					<th>firstname</th>
					<th>lastname</th>
					<th>email</th>
					<th>ssn</th>
					<th>role</th>
					<th></th>
				</tr>
			</thead>
			<tbody>
				<c:forEach items="${users}" var="user">
					<tr>
						<td>${user.userid}</td>
						<td>${user.username}</td>
						<td>${user.firstname}</td>
						<td>${user.lastname}</td>						
						<td>${user.email}</td>
						<td>${user.ssn}</td>
						<td><a type="button" class="btn btn-primary"
							href="/update-user?userid=${user.userid}">Update</a></td>
						<td><a type="button" class="btn btn-danger"
							href="/delete-user?userid=${user.userid}">Delete</a></td>
					</tr>
				</c:forEach>
			</tbody>
		</table>

	</div>
<%@ include file="common/footer.jspf" %>