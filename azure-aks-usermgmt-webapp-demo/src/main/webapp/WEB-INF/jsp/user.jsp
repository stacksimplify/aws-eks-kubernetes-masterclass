<%@ include file="common/header.jspf" %>
<%@ include file="common/navigation.jspf" %>
<div class="page-header">
  <h2 class="text-center">Create User</h2>
</div>
<div class="container">
	<form:form method="post" modelAttribute="user">
		<form:hidden path="userid" />

		<fieldset class="form-group">
			<form:label path="username">User Name</form:label>
			<form:input path="username" type="text" class="form-control"
				required="required" />
			<form:errors path="username" cssClass="text-warning" />
		</fieldset>
		
		<fieldset class="form-group">
			<form:label path="password">Password</form:label>
			<form:input path="password" type="text" class="form-control"
				required="required" />
			<form:errors path="password" cssClass="text-warning" />
		</fieldset>
		
		
		<fieldset class="form-group">
			<form:label path="firstname">First Name</form:label>
			<form:input path="firstname" type="text" class="form-control"
				required="required" />
			<form:errors path="firstname" cssClass="text-warning" />
		</fieldset>

		<fieldset class="form-group">
			<form:label path="lastname">Last Name</form:label>
			<form:input path="lastname" type="text" class="form-control"
				required="required" />
			<form:errors path="lastname" cssClass="text-warning" />
		</fieldset>

		<fieldset class="form-group">
			<form:label path="email">Email Address</form:label>
			<form:input path="email" type="text" class="form-control"
				required="required" />
			<form:errors path="email" cssClass="text-warning" />
		</fieldset>

		<fieldset class="form-group">
			<form:label path="ssn">Social Security Number</form:label>
			<form:input path="ssn" type="text" class="form-control"
				required="required" />
			<form:errors path="ssn" cssClass="text-warning" />
		</fieldset>
		
		

<!--  Will fix permanent roles later
		<fieldset class="form-group">
			<form:label path="roles">Roles</form:label>
			<form:errors path="roles" cssClass="text-warning" />
			<form:select path="roles" items="${roles}" 
			multiple="true" itemValue="roleid" 
			itemLabel="type" 
			class="form-control" />
		</fieldset>		
 -->
 
 				<c:choose>
					<c:when test="${edit}">
						<input type="submit" value="Update" class="btn btn-primary"/> 
						<a value="Cancel" class="btn btn-primary" href="<c:url value='/list-users' />">Cancel</a>
					</c:when>
					<c:otherwise>
						<input type="submit" value="Add" class="btn btn-primary "/> 
						<a value="Cancel" class="btn btn-primary" href="<c:url value='/list-users' />">Cancel</a>
					</c:otherwise>
				</c:choose>
 

						<!--  <button type="submit" class="btn btn-success">Add</button> -->
							
	</form:form>
</div>
<%@ include file="common/footer.jspf" %>