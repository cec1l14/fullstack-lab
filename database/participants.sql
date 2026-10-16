SELECT users.name
from registrations
join users on users.id = registrations.user_id
where registrations.event_id = :event_id
order by users.name asc;