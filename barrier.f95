! try to  make something work with barrier breach
program barrier

implicit none
integer, parameter :: dp = selected_real_kind(15, 307)
real :: slope, beach
real, allocatable, dimension(:) :: bathy, row
!integer, dimension(5:5) :: test
integer :: i, j, mx, my , n, t1, t2, bathy_size, rowidx, colidx, idx, jdx, ip, jp
real :: xll, yll, cellsize, nodata_value, amp_max, dx, sigma, h0, x1, x2, col, stepx, stepy
real :: time(10) != (/(i, i=0,9, 1)/)
real, dimension(10) :: amp
real, dimension(1:10) :: time_test
integer, dimension(10) :: zero_array
integer, dimension(10) :: one_array
real(kind=8) :: values(10)
character(len=80) :: str

real, dimension(600) :: y 
real,allocatable, dimension(:,:) :: X_mesh, Y_mesh, breach, test
real, dimension(500) :: x 
stepx = (100.0 + 100.0)/ real(499.0, dp)
stepy = (60e3 / real(599, dp))
x = (/((i-1)*stepx -100.0, i=1,500)/)
y = (/((i-1)* stepy + 0, i=1, 600)/)
 !x = [(i*dx+a, i = 0, n-1)]
 do idx=1, size(x)
	print *, idx, x(idx)
	end do
print *,'the index of x and y are 0?', x(1), y(599)
open(10, file='test.tt3')
	read(10,*) mx
	read(10,*) my
	read(10,*) xll
	read(10,*) yll
	read(10,*) cellsize
	read(10,*) nodata_value
close(10)
t1 = 3.0
t2 = 6.0
amp_max = 5.0
dx = 10.0/9.0 !((10) / (9))
time(1:10) = [(0 + ((i-1)*dx),i=1, 10)]

zero_array = 0
one_array = 1

do i = 1, 10
	if (time(i) < t1) then
		amp(i) = zero_array(i)
	elseif (t1 <= time(i) .and. time(i) < t2) then
		amp(i) =  (amp_max / (t2 - t1) * (time(i) - t1))
	elseif (t2 <= time(i)) then
		amp(i) = one_array(i) * amp_max
end if
	
end do


print *, 'This has run'
! print *,  SHAPE(bathy)
! allocate(bathy(1:mx*my))
! allocate(breach(1:bathy_size))
! open(11, file='test.tt3')
! do i=1,6
    ! read(11, *)
! end do
! print *, 'no error here'

! do j=1, my !*nrows
   ! read(11, *) (bathy((j-1)* mx + i),i=1,mx)
! end do
! print *, bathy(1:my*mx)
sigma = 10.0
test(:,:) = spread(x, 1, size(y))
! do idx = 1, size(x)
! print*, test(1,idx)
! end do
print *,'rank of x & y',  rank(x), rank(y)
allocate(X_mesh(size(y), size(x)))
allocate(Y_mesh(size(y), size(x)))
do i=1, size(y)
	do j=1, size(x)
		X_mesh(i,j) = x(j)
		Y_mesh(i,j) = y(i)
	end do
end do
print *, Y_mesh(75, 221)
x1 = -25.0
x2 = 25.0
! do idx=0,size(X_mesh,2)
	! print *, idx, X_mesh(1,idx)
	! end do
!print *, size(X_mesh,1), size(X_mesh, 2)
! do i=1, size(X_mesh, 1)
! print *, size(X_mesh(i,:))
print *, size( X_mesh, 1)
allocate(breach(size(X_mesh, 1), size(X_mesh, 2)))
do i= 1, size(X_mesh,2)
	breach(:,i) = 10
	do j = 1, size(X_mesh,1)
		breach(j,:) = 10
end do
end do
print*, 'X', shape(X_mesh), 'Y', shape(Y_mesh), 'B', shape(breach), 'the size of X(mesh, 2) is', size(X_mesh, 2)
print *, 'X_mesh, 1', X_mesh(1,499)
do i = 1, size(amp)
	print *, 'amp loop', i
	do rowidx = 1, size(X_mesh, 1)
	!print *, 'row', rowidx
		row = X_mesh(rowidx,:)
			do colidx = 1, size(X_mesh, 2)
	!			print *, 'col', colidx
				col = X_mesh(rowidx, colidx)
				
				if (col >= x1 .and. col <= x2) then
					!print *, 'breaching'
					!print*, Y_mesh(rowidx, colidx)
					breach(rowidx, colidx) = breach(rowidx, colidx) - (amp(i) * exp(-X_mesh(rowidx, colidx)**2/(sigma**2)) &
					* 0.1 * Y_mesh(rowidx, colidx))
					
				end if
				
			end do
	end do

print '("Matrix Breach"/(10F8.2))', ((breach(ip,jp), ip = 112, 129), jp = 187, 192) 
open(99, file='fortran_test.txt', status='replace', action='write')


 ! READ (10, *)  ((B(i, j), i = 1, 4), j = 1, 4)  
write(99, "(10F16.8)") ((breach(jp,ip), ip = 1, size(breach, 2)), jp = 1, size(breach, 1))
! do idx=1, size(X_mesh, 2)
	! do jdx = 1, size(X_mesh, 1)
		! write(99,*) breach(idx,jdx)
	! end do
! end do
close(99)

	!where (any(x1 <= X_mesh(:,:) .and. X_mesh(:,:) <= x2))
	!print *, amp(i)
		!breach = breach - amp(i) * exp(-X_mesh**2 / sigma**2) * 0.10 * Y_mesh
	!end where
end do

!print *, breach
end program barrier
